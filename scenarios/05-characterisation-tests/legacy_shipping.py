# legacy_shipping.py — "written in 2015, nobody remembers why" (scenario 5)
# Deliberately left as it was found: no type hints, magic numbers, quirks.
# Characterisation tests record what it does TODAY before anyone changes it.

RATES = {
    "A": (4.50, 0.80, 0.60, 0.45),   # base fee, per kg <=5, per kg <=20, per kg >20
    "B": (6.00, 1.10, 0.85, 0.70),
    "C": (9.50, 1.60, 1.30, 1.05),
}


def shipping_cost(weight, zone, express=False):
    base, r1, r2, r3 = RATES[zone]
    if weight <= 0:
        cost = base
    elif weight <= 5:
        cost = base + weight * r1
    elif weight < 20:
        cost = base + weight * r2
    else:
        cost = base + weight * r3
    if express:
        cost = cost * 1.5 + 5
    return round(cost, 2)
