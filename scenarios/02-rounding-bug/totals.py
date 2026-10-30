"""The fixed invoice total, implementing finance's stated rule.

Rule (confirmed with finance at the human checkpoint in scenario 2):
- amounts are decimal, never float;
- each line (quantity x unit price) is rounded half-up to cents;
- the invoice total is the sum of the rounded lines.
"""
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def line_amount(quantity, unit_price) -> Decimal:
    return (Decimal(quantity) * Decimal(str(unit_price))).quantize(CENT, rounding=ROUND_HALF_UP)


def invoice_total(lines) -> Decimal:
    """lines: iterable of (quantity, unit_price) pairs. Prices as str or Decimal."""
    return sum((line_amount(q, p) for q, p in lines), Decimal("0.00"))
