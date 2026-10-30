"""Reproduce the five reported invoices first, then fix (scenario 2)."""
from decimal import Decimal

import pytest
import totals
import totals_buggy

# The five sample invoices from the bug report: lines and finance's figure.
SAMPLES = {
    "invoice-1": ([(1, "0.105"), (1, "0.105")], "0.22"),
    "invoice-2": ([(3, "1.115")], "3.35"),
    "invoice-3": ([(1, "1.005")], "1.01"),
    "invoice-4": ([(1, "2.675")], "2.68"),
    "invoice-5": ([(7, "0.145"), (1, "99.99")], "101.01"),
}


@pytest.mark.parametrize("name", SAMPLES)
def test_fixed_total_matches_finance(name):
    lines, expected = SAMPLES[name]
    assert totals.invoice_total(lines) == Decimal(expected)


@pytest.mark.parametrize("name", SAMPLES)
def test_buggy_total_is_one_cent_off(name):
    """Documents the bug: every sample differs by exactly one cent."""
    lines, expected = SAMPLES[name]
    diff = abs(Decimal(str(totals_buggy.invoice_total(lines))) - Decimal(expected))
    assert diff == Decimal("0.01")


def test_round_total_only_is_not_the_fix():
    """The tempting wrong fix: Decimal, but rounding only the total.

    It happens to fix invoice-2 and still gets invoice-1 wrong, which is why
    the rule had to come from finance, not from the five samples.
    """
    def round_total_only(lines):
        total = sum(Decimal(q) * Decimal(p) for q, p in lines)
        return total.quantize(totals.CENT, rounding="ROUND_HALF_UP")

    assert round_total_only(SAMPLES["invoice-2"][0]) == Decimal("3.35")
    assert round_total_only(SAMPLES["invoice-1"][0]) != Decimal("0.22")


def test_ordinary_invoices_are_unchanged():
    lines = [(2, "19.99"), (1, "5.00"), (10, "0.50")]
    assert totals.invoice_total(lines) == Decimal("49.98")
    assert totals_buggy.invoice_total(lines) == 49.98
