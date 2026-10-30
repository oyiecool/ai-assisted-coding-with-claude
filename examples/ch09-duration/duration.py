"""parse_duration — the test-first example from Chapter 9.

Specification (section 9.1, with the decisions made in section 9.6):
- "1h30m" -> 5400 seconds. Units h, m and s, in any order, each at most once.
- Whole non-negative numbers only: no decimals, no signs.
- No whitespace anywhere.
- Empty strings, unknown units and repeated units raise ValueError.
"""
import re

UNIT_SECONDS = {"h": 3600, "m": 60, "s": 1}
_TOKEN = re.compile(r"(\d+)([hms])")


def parse_duration(text: str) -> int:
    if not isinstance(text, str) or not text:
        raise ValueError("duration must be a non-empty string")
    tokens = _TOKEN.findall(text)
    if "".join(number + unit for number, unit in tokens) != text:
        raise ValueError(f"invalid duration: {text!r}")
    units = [unit for _, unit in tokens]
    if len(units) != len(set(units)):
        raise ValueError(f"repeated unit in duration: {text!r}")
    return sum(int(number) * UNIT_SECONDS[unit] for number, unit in tokens)
