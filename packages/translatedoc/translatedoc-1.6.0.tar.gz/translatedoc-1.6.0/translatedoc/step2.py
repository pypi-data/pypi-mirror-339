#!/usr/bin/env python3
"""翻訳処理部分だけ切り出したもの。"""

import argparse
import importlib.metadata
import logging
import os
import pathlib
import sys
import typing

import openai
import pytilpack.tqdm_
import tiktoken
import tqdm

from translatedoc import utils

from .step1 import regex_newline3

logger = logging.getLogger(__name__)


def main():
    """メイン関数。"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[pytilpack.tqdm_.TqdmStreamHandler()],
    )

    parser = argparse.ArgumentParser(description="Translate text file.")
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
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose mode")
    parser.add_argument(
        "input_files", nargs="*", help="input text files", type=pathlib.Path
    )
    parser.add_argument("--version", "-V", action="store_true", help="show version")
    args = parser.parse_args()
    if args.version:
        print(f"translatedoc {importlib.metadata.version('translatedoc')}")
        sys.exit(0)
    if len(args.input_files) == 0:
        parser.error("at least one input file is required")
    utils.set_verbose(args.verbose)

    openai_client = openai.OpenAI(api_key=args.api_key, base_url=args.api_base)

    exit_code = 0
    for input_path in tqdm.tqdm(args.input_files, desc="Input files/URLs"):
        try:
            # テキストファイルの読み込み
            text = input_path.read_text(encoding="utf-8")

            # 翻訳
            output_path = (
                args.output_dir / input_path.with_suffix(f".{args.language}.txt").name
            )
            if utils.check_overwrite(output_path, args.force):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with output_path.open("w") as file:
                    logger.info(f"Translating {input_path}...")
                    chunks = partition(text, args.model)
                    for chunk in tqdm.tqdm(chunks, desc="Chunks"):
                        output_chunk = translate(
                            str(chunk), args.model, args.language, openai_client
                        )
                        file.write(f"{output_chunk}\n\n")
                        file.flush()
                logger.info(f"{output_path} written.")
        except Exception as e:
            logger.error(f"{e} ({input_path})")
            exit_code = 1

    sys.exit(exit_code)


def partition(text: str, model: str, max_chunk_size: int | None = None) -> list[str]:
    """翻訳用に分割する。"""
    # 最大チャンクサイズの決定: 翻訳前提ならコンテキスト長の1/3くらいでいい気もするが安全を見て1/4
    if max_chunk_size is None:
        system_prompt_tokens = 100  # システムプロンプトの大体のトークン数
        max_tokens = max_tokens_from_model_name(model)
        logger.debug(f"{max_tokens=}")
        max_chunk_size = (max_tokens - system_prompt_tokens) // 4
        max_chunk_size = min(max_chunk_size, 1000)  # 長すぎても抜けが多くなるっぽいので
        logger.debug(f"{max_chunk_size=}")

    encoding = tiktoken.encoding_for_model(model)

    def count_tokens(x: str) -> int:
        return len(encoding.encode(x))

    # 基本は改行3つ以上で区切る
    base_parts = regex_newline3.split(text)

    # max_chunk_sizeを超えないトークン数ずつチャンクにしていく
    chunks: list[str] = []
    for base_part in base_parts:
        if count_tokens(base_part) <= max_chunk_size:
            # max_chunk_size以下ならそのまま追加
            chunks.append(base_part)
        else:
            # base_partを更に分割
            chunk = ""
            for part in _sub_partition(base_part, max_chunk_size, count_tokens):
                # 今回のpartを追加するとチャンクサイズを超える場合、いったんそこで区切る
                if count_tokens(chunk + part) > max_chunk_size:
                    assert chunk != ""
                    chunks.append(chunk)
                    chunk = ""
                # チャンクに追加する
                chunk += part
            if chunk != "":
                chunks.append(chunk)

    return _merge_chunks(chunks, max_chunk_size, count_tokens)


def _merge_chunks(
    chunks: list[str], max_chunk_size: int, count_tokens: typing.Callable[[str], int]
) -> list[str]:
    """複数のチャンクを結合してもmax_chunk_size以下なところは結合していく。"""
    chunk_sep = "\n\n\n"

    combined_chunks: list[str] = []
    combined_chunk = ""
    last_chunk = ""
    for chunk in chunks:
        # 今回のチャンクを追加するとチャンクサイズを超える場合、いったんそこで区切る
        # また、今回のチャンクが直前のチャンクより大幅に短い場合もタイトルの可能性があるので区切る
        # (もうちょっと賢くしたい気もするがとりあえず)
        if (
            count_tokens(combined_chunk + chunk_sep + chunk) > max_chunk_size
            or len(chunk) <= len(last_chunk) // 8
        ):
            assert combined_chunk != ""
            combined_chunks.append(combined_chunk)
            combined_chunk = ""
        # combined_chunkに追加する (セパレーター付き)
        if combined_chunk != "":
            combined_chunk += chunk_sep
        combined_chunk += chunk
        last_chunk = chunk

    # 最後のチャンク
    if combined_chunk != "":
        combined_chunks.append(combined_chunk)

    return combined_chunks


def _sub_partition(
    text: str,
    max_chunk_size: int,
    count_tokens: typing.Callable[[str], int],
    separator="\n\n",
) -> list[str]:
    """textをmax_chunk_sizeを超えないサイズに分割していく。"""
    parts: list[str] = []

    # 基本は改行2つ以上で区切る
    # 改行区切りである程度分かれるならそれ単位
    # それでもだめならスペース区切り
    # 最終手段として区切りを考えず
    next_separator = {"\n\n": "\n", "\n": " ", " ": ""}[separator]

    # separatorで分割して1つずつ見ていく
    for part in split_with_separator(text, separator):
        assert part != ""
        # max_chunk_size以下ならOK
        if count_tokens(part) <= max_chunk_size:
            parts.append(part)
            continue

        # 超えてたらセパレーターを変えて再帰的に更に分割
        if next_separator != "":
            sub_parts = _sub_partition(
                part, max_chunk_size, count_tokens, next_separator
            )
            parts.extend(sub_parts)
            continue

        # 最終手段、文字単位でぶつ切り
        sub_part = ""
        for c in part:
            # 今回の文字を追加するとチャンクサイズを超える場合、いったんそこで区切る
            if count_tokens(sub_part + c) > max_chunk_size:
                parts.append(sub_part)
                sub_part = ""
            # 今回の文字を今の塊(sub_part)に追加
            sub_part += c
        if sub_part != "":
            parts.append(sub_part)

    return parts


def split_with_separator(text: str, separator: str) -> list[str]:
    """separatorで分割し、separatorを含めて返す。"""
    splitted: list[str] = []
    index = 0
    while True:
        next_index = text.find(separator, index)
        if next_index == -1:
            break
        next_index += len(separator)
        splitted.append(text[index:next_index])
        index = next_index
    splitted.append(text[index:])
    return splitted


def translate(
    chunk: str, model: str, language: str, openai_client: openai.OpenAI
) -> str:
    """翻訳。"""
    chunk = chunk.strip()
    logger.debug(f"Translating input:\n{chunk}\n\n")
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Translate the all inputs into {language}.\n"
                "Translate everything without omission.\n"
                "Do not output anything other than the translation result.\n"
                "Do not translate names of people, mathematical formulas,"
                " source code, URLs, etc.\n",
            },
            {"role": "user", "content": f"```\n{chunk}\n```"},
        ],
        temperature=0.0,
    )
    result: str
    if len(response.choices) != 1 or response.choices[0].message.content is None:
        result = f"*** Unexpected response: {response.model_dump()=} ***"
    else:
        result = response.choices[0].message.content.strip()

    if result.startswith("```\n"):
        result = result[4:]
    if result.endswith("\n```"):
        result = result[:-4]
    result = result.strip()

    logger.debug(f"Translated output:\n{result}\n\n")
    return result


def max_tokens_from_model_name(model: str) -> int:
    """OpenAIのモデル名から最大トークン数を返す。

    Args:
        model: モデル名。

    Returns:
        最大トークン数。

    """
    max_tokens = MODEL_MAX_TOKENS.get(model)
    if max_tokens is None:
        logger.warning(f"Unknown model: {model}")
        if "gpt-4" in model:
            return 8192
        return 4096
    return max_tokens


# https://platform.openai.com/docs/models/gpt-3-5-turbo
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
MODEL_MAX_TOKENS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-0125": 16385,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-16k-0613": 16385,
    "gpt-3.5-turbo-instruct": 4096,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0613": 32768,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-vision-preview": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4o": 128000,
    "gpt-4o-2024-05-13": 128000,
    "gpt-4o-2024-08-06": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
    "chatgpt-4o-latest": 128000,
}

if __name__ == "__main__":
    main()
