"""テストコード。"""

import pathlib

import translatedoc

TEST_DATA_DIR = pathlib.Path(__file__).parent / "data"


def test_split_with_separator():
    """区切り文字付き文字列分割のテスト。"""
    text = "Hello World.  How are you?"
    parts = translatedoc.split_with_separator(text, " ")
    assert parts == ["Hello ", "World. ", " ", "How ", "are ", "you?"], repr(parts)


def test_partition1():
    """分割テストその1。"""
    text = """
a a a


a a a


a


a
"""
    chunks = translatedoc.partition(text.strip(), "gpt-3.5-turbo", max_chunk_size=5)
    assert chunks == ["a a a", "a a a\n\n\na", "a"], repr(chunks)


def test_partition2():
    """分割テストその2。"""
    text = """
a a a


b b b b b b


とてもとても長いテキスト
"""
    chunks = translatedoc.partition(text.strip(), "gpt-3.5-turbo", max_chunk_size=5)
    assert chunks == [
        "a a a",
        "b b b b ",
        "b b",
        "とてもとて",
        "も長いテ",
        "キスト",
    ], repr(chunks)


def test_partition3():
    """分割テストその3。"""
    # 情報が欠落・重複してないことの確認
    text = (TEST_DATA_DIR / "2402.04494.Source.txt").read_text(encoding="utf-8")
    chunks = translatedoc.partition(text, "gpt-3.5-turbo-0613")
    assert "".join(text.split("\n")) == "".join("".join(chunks).split("\n"))

    text = (TEST_DATA_DIR / "2401.15422.Source.txt").read_text(encoding="utf-8")
    chunks = translatedoc.partition(text, "gpt-3.5-turbo-0125")
    assert "".join(text.split("\n")) == "".join("".join(chunks).split("\n"))
