import pytest
from duration import parse_duration

@pytest.mark.parametrize("text, expected", [
    ("1h", 3600),
    ("30m", 1800),
    ("45s", 45),
    ("1h30m", 5400),
    ("30m1h", 5400),          # any order
    ("2h0m5s", 7205),
    ("0s", 0),
])
def test_valid(text, expected):
    assert parse_duration(text) == expected

@pytest.mark.parametrize("text", [
    "",        # empty
    "-5m",     # negative
    "5d",      # unknown unit
    "1h1h",    # repeated unit
    "h",       # missing number
    "1.5h",    # decimals not allowed by spec
    " 1h",     # whitespace not allowed by spec
])
def test_invalid(text):
    with pytest.raises(ValueError):
        parse_duration(text)
