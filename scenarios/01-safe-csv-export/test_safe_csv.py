import csv
import io
import itertools
from decimal import Decimal

import pytest
from safe_csv import iter_csv, safe_cell


@pytest.mark.parametrize("value", [
    '=HYPERLINK("http://evil.example","Click")',
    "+1+1", "-2+3", "@SUM(A1:A9)", "\t=1", "\r=1",
])
def test_dangerous_text_is_neutralised(value):
    assert safe_cell(value) == "'" + value


@pytest.mark.parametrize("value, expected", [
    ("Acme Ltd", "Acme Ltd"),
    ("", ""),
    (None, ""),
    ("a=b", "a=b"),              # only a LEADING character is dangerous
    (-42, -42),                  # numbers stay numeric
    (Decimal("-10.50"), Decimal("-10.50")),
])
def test_safe_values_are_unchanged(value, expected):
    assert safe_cell(value) == expected


def test_quoting_is_left_to_the_csv_module():
    text = "".join(iter_csv(["name"], [['He said "hi", then left']]))
    assert list(csv.reader(io.StringIO(text)))[1] == ['He said "hi", then left']


def test_header_is_protected_too():
    first = next(iter_csv(["=cmd"], []))
    assert first.startswith("'=cmd")


def test_streams_lazily_without_reading_all_rows():
    consumed = 0

    def rows():
        nonlocal consumed
        for i in itertools.count():
            consumed += 1
            yield [i, f"row {i}"]

    stream = iter_csv(["id", "name"], rows())   # an infinite source
    lines = list(itertools.islice(stream, 3))   # header + 2 rows
    assert len(lines) == 3
    assert consumed == 2


def test_100k_rows():
    rows = ([i, f"customer {i}", Decimal("1.00")] for i in range(100_000))
    count = sum(1 for _ in iter_csv(["id", "name", "amount"], rows))
    assert count == 100_001
