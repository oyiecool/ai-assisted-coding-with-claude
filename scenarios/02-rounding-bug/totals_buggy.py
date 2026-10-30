"""The original invoice total: floats, and one round() at the end.

Two separate problems hide here:
1. Binary floating point cannot represent most decimal amounts exactly,
   so 3 x 1.115 is 3.3449999..., not 3.345.
2. Finance's rule is "round each line half-up to cents, then add the
   lines". This code rounds only the total, and Python's round() uses
   round-half-to-even on whatever float it is given.
"""


def invoice_total(lines):
    """lines: iterable of (quantity, unit_price) pairs. Returns a float."""
    return round(sum(qty * float(price) for qty, price in lines), 2)
