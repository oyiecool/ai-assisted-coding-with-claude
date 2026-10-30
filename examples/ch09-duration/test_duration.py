"""Tests written BEFORE the implementation, as in sections 9.1 and 9.6."""
import pytest
from duration import parse_duration
from hypothesis import given
from hypothesis import strategies as st


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
    "1h ",
    "+5m",
    "10",      # number without unit
])
def test_invalid(text):
    with pytest.raises(ValueError):
        parse_duration(text)


# Section 9.7: a property-based round-trip test.
@given(h=st.integers(0, 99), m=st.integers(0, 59), s=st.integers(0, 59))
def test_roundtrip(h, m, s):
    text = f"{h}h{m}m{s}s"
    assert parse_duration(text) == h * 3600 + m * 60 + s


@given(st.permutations(["2h", "3m", "4s"]))
def test_order_does_not_matter(parts):
    assert parse_duration("".join(parts)) == 2 * 3600 + 3 * 60 + 4


@given(st.text(max_size=12))
def test_never_crashes_with_unexpected_errors(text):
    """Any string either parses to a non-negative int or raises ValueError."""
    try:
        assert parse_duration(text) >= 0
    except ValueError:
        pass
