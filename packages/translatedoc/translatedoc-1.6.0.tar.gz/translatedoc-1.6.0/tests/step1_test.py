"""テストコード。"""

import pathlib

import translatedoc

TEST_DATA_DIR = pathlib.Path(__file__).parent / "data"


def test_extract_text_markdown():
    """テキスト抽出テストその1。

    uv run translatedoc-step1 tests/data/markdown.md
    cat markdown.Source.txt
    mv -f markdown.Source.txt tests/data/

    """
    text = translatedoc.extract_text(TEST_DATA_DIR / "markdown.md")
    expected = (TEST_DATA_DIR / "markdown.Source.txt").read_text()
    assert text == expected
