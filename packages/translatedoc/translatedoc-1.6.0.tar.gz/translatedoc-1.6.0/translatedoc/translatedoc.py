#!/usr/bin/env python3
"""translatedoc - ドキュメントを翻訳するツール。"""

import argparse
import importlib.metadata
import logging
import os
import pathlib
import sys

import openai
import pytilpack.tqdm_
import tqdm

from translatedoc import extract_text, partition, translate, utils

logger = logging.getLogger(__name__)


def main():
    """メイン関数。"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[pytilpack.tqdm_.TqdmStreamHandler()],
    )

    parser = argparse.ArgumentParser(
        description="Extract text from documents and translate it."
    )
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
        "--language",
        "-l",
        default="Japanese",
        help="target language name (default: Japanese)",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (default: OPENAI_API_KEY environment variable)",
    )
    parser.add_argument(
        "--api-base",
        "-b",
        default=os.environ.get("OPENAI_API_BASE"),
        help="OpenAI API base URL (default: OPENAI_API_BASE environment variable)",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=os.environ.get("TRANSLATEDOC_MODEL", "gpt-4o-mini"),
        help="model (default: gpt-4o-mini)",
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

    openai_client = openai.OpenAI(api_key=args.api_key, base_url=args.api_base)

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

            # 動作確認用: --language=noneで翻訳をスキップ
            if args.language.lower() == "none":
                continue

            # 翻訳
            output_path = (
                args.output_dir / input_path.with_suffix(f".{args.language}.txt").name
            )
            if utils.check_overwrite(output_path, args.force):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with output_path.open("w") as file:
                    logger.info(f"Translating {input_file}...")
                    chunks = partition(text, args.model)
                    for chunk in tqdm.tqdm(chunks, desc="Chunks"):
                        output_chunk = translate(
                            str(chunk), args.model, args.language, openai_client
                        )
                        file.write(f"{output_chunk}\n\n")
                        file.flush()
                logger.info(f"{output_path} written.")
        except Exception as e:
            logger.error(f"{e} ({input_file})")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
