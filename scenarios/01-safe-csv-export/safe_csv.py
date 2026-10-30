"""Streaming CSV export with CSV-injection protection (scenario 1).

Spreadsheet applications treat a cell that starts with =, +, -, @, tab or
carriage return as a formula. A malicious value such as
=HYPERLINK("http://evil.example","Click") then runs when someone opens the
export. safe_cell() neutralises those cells by prefixing a single quote,
which spreadsheets display as text. Numbers are left alone so that negative
amounts stay numeric.
"""
from __future__ import annotations

import csv
import io
from collections.abc import Iterable, Iterator
from decimal import Decimal

DANGEROUS_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value: object) -> object:
    """Return a value that is safe to write to a CSV cell."""
    if value is None:
        return ""
    if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
        return value
    text = str(value)
    if text.startswith(DANGEROUS_PREFIXES):
        return "'" + text
    return text


def iter_csv(header: list[str], rows: Iterable[Iterable[object]]) -> Iterator[str]:
    """Yield the CSV one line at a time; rows are consumed lazily.

    Suitable for a streaming HTTP response: memory use does not grow with
    the number of rows.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    def flush() -> str:
        line = buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)
        return line

    writer.writerow([safe_cell(h) for h in header])
    yield flush()
    for row in rows:
        writer.writerow([safe_cell(v) for v in row])
        yield flush()
