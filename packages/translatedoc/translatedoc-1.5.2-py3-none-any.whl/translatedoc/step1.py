#!/usr/bin/env python3
"""テキスト抽出部分だけ切り出したもの。"""

import argparse
import importlib.metadata
import logging
import os
import pathlib
import re
import sys
import typing

import markdownify
import pytilpack.tqdm_
import tqdm

from translatedoc import utils

logger = logging.getLogger(__name__)

regex_newline3 = re.compile(r"\n{3,}")


def main():
    """メイン関数。"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[pytilpack.tqdm_.TqdmStreamHandler()],
    )

    parser = argparse.ArgumentParser(description="Extract text from documents.")
    parser.add_argument(
        "--output-dir",
        "-o",
        default=pathlib.Path("."),
        type=pathlib.Path,
        help="output directory (default: .)",
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="overwrite existing files"
    )
    parser.add_argument(
        "--strategy",
        "-s",
        choices=["auto", "fast", "ocr_only", "hi_res"],
        default=os.environ.get("TRANSLATEDOC_STRATEGY", "hi_res"),
        help="document partitioning strategy (default: hi_res)",
        # hi_resはtesseractやdetectron2を使うので重いけど精度が高いのでデフォルトに
    )
    parser.add_argument(
        "--all-elements",
        "-a",
        action="store_true",
        help="output all elements (default: remove header/footer)",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="verbose mode")
    parser.add_argument("input_files", nargs="*", help="input files/URLs")
    parser.add_argument("--version", "-V", action="store_true", help="show version")
    args = parser.parse_args()
    if args.version:
        print(f"translatedoc {importlib.metadata.version('translatedoc')}")
        sys.exit(0)
    if len(args.input_files) == 0:
        parser.error("at least one input file/URL is required")
    utils.set_verbose(args.verbose)

    exit_code = 0
    for input_file in tqdm.tqdm(args.input_files, desc="Input files/URLs"):
        input_path = pathlib.Path(input_file)
        try:
            # テキスト抽出
            logger.info(f"Loading {input_file}...")
            text = extract_text(input_file, args.strategy, args.all_elements)
            source_path = args.output_dir / input_path.with_suffix(".Source.txt").name
            if utils.check_overwrite(source_path, args.force):
                source_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.write_text(text, encoding="utf-8")
                logger.info(f"{source_path} written.")
        except Exception as e:
            logger.error(f"{e} ({input_file})")
            exit_code = 1

    sys.exit(exit_code)


def extract_text(
    input_file: str | pathlib.Path, strategy: str = "auto", all_elements: bool = False
) -> str:
    """テキスト抽出。

    Args:
        input_file: 入力ファイルパスまたはURL。
        strategy: ドキュメント分割戦略。

    """
    # timmのimport時にSegmentation Faultが起きることがあるようなのでとりあえず暫定対策
    # https://github.com/invoke-ai/InvokeAI/issues/4041
    os.environ["PYTORCH_JIT"] = "0"

    # unstructuredでテキスト抽出
    input_file = str(input_file)
    kwargs: typing.Mapping[str, typing.Any] = (
        {"url": input_file}
        if input_file.startswith("http://") or input_file.startswith("https://")
        else {"filename": input_file}
    )
    with tqdm.tqdm.external_write_mode():
        from unstructured.chunking.title import chunk_by_title
        from unstructured.documents.elements import Text as TextElement
        from unstructured.partition.auto import partition

        elements = partition(strategy=strategy, skip_infer_table_types=[], **kwargs)

    if logger.isEnabledFor(logging.DEBUG):
        for i, el in enumerate(elements):
            logger.debug(f"Element[{i + 1}/{len(elements)}]: {el.category} ({el})")

    # None, Image, Header, Footerを削除
    elements = [el for el in elements if el is not None]
    if not all_elements:
        elements = [
            el for el in elements if el.category not in ("Image", "Header", "Footer")
        ]

    # テーブルをTextElement化
    for i, el in enumerate(elements):
        if el.metadata is not None and el.metadata.text_as_html is not None:
            markdown_text = markdownify.markdownify(el.metadata.text_as_html).strip()
            elements[i] = TextElement(text=markdown_text)

    # タイトルで分割
    chunks = chunk_by_title(
        elements, combine_text_under_n_chars=0, max_characters=2**31 - 1
    )
    chunks = [str(c).strip() for c in chunks]
    chunks = [regex_newline3.sub("\n\n", c) for c in chunks]
    if logger.isEnabledFor(logging.DEBUG):
        for i, chunk in enumerate(chunks):
            logger.debug(f"Chunk[{i + 1}/{len(chunks)}]:\n{chunk}\n\n")

    return "\n\n\n".join(chunks) + "\n"


if __name__ == "__main__":
    main()
