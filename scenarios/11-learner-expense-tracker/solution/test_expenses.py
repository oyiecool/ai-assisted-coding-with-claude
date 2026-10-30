from decimal import Decimal
from pathlib import Path

import pytest
from expenses import by_category, by_month, read_expenses, report

SAMPLE = Path(__file__).parent.parent / "expenses.csv"


@pytest.fixture
def rows():
    good, _ = read_expenses(SAMPLE)
    return good


def test_reads_good_rows_and_reports_bad_ones():
    good, problems = read_expenses(SAMPLE)
    assert len(good) == 9
    assert len(problems) == 2
    assert any("bad amount" in p for p in problems)
    assert any("bad date" in p for p in problems)


def test_totals_by_category(rows):
    totals = by_category(rows)
    assert totals["Groceries"] == Decimal("142.30")
    assert totals["Transport"] == Decimal("38.50")


def test_totals_by_month(rows):
    totals = by_month(rows)
    assert list(totals) == ["2026-09", "2026-10"]
    assert sum(totals.values()) == sum(by_category(rows).values())


def test_report_mentions_skipped_rows():
    text = report(SAMPLE)
    assert "By category:" in text and "Skipped 2 bad row(s)" in text


def test_a_broken_total_would_be_caught(rows, monkeypatch):
    """Break the code on purpose: drop the last row. A good test fails."""
    assert by_category(rows[:-1]) != by_category(rows)
