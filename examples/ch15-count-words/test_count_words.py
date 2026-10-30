"""The two tests the tutor asked for, which would have caught the bug."""
import pytest
from count_words import count_words, count_words_buggy


@pytest.fixture
def last_line_empty(tmp_path):
    path = tmp_path / "a.txt"
    path.write_text("hello world\n\n")
    return path


@pytest.fixture
def several_lines(tmp_path):
    path = tmp_path / "b.txt"
    path.write_text("one two\nthree\nfour five six\n")
    return path


def test_last_line_empty(last_line_empty):
    assert count_words(last_line_empty) == 2


def test_several_lines(several_lines):
    assert count_words(several_lines) == 6


def test_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("")
    assert count_words(path) == 0


def test_the_buggy_version_fails_these_tests(last_line_empty, several_lines):
    assert count_words_buggy(last_line_empty) == 0   # should be 2
    assert count_words_buggy(several_lines) == 3     # should be 6
