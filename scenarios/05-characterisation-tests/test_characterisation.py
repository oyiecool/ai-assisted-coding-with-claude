"""Characterisation tests for legacy_shipping.shipping_cost (scenario 5).

These record what the function returns TODAY. They are not a statement of
what it SHOULD return. Results that looked wrong are listed separately at
the bottom, marked SURPRISE, for a human to decide.

To check the safety net works: change one rate in RATES and confirm that
at least one test fails.
"""
import pytest
from legacy_shipping import shipping_cost

RECORDED = [
    # weight, zone, express, cost today
    (0, "A", False, 4.5),
    (0, "A", True, 11.75),
    (0.5, "A", False, 4.9),
    (0.5, "A", True, 12.35),
    (1, "A", False, 5.3),
    (1, "A", True, 12.95),
    (5, "A", False, 8.5),
    (5, "A", True, 17.75),
    (5.01, "A", False, 7.51),
    (5.01, "A", True, 16.26),
    (10, "A", False, 10.5),
    (10, "A", True, 20.75),
    (19.99, "A", False, 16.49),
    (19.99, "A", True, 29.74),
    (20, "A", False, 13.5),
    (20, "A", True, 25.25),
    (20.01, "A", False, 13.5),
    (20.01, "A", True, 25.26),
    (35, "A", False, 20.25),
    (35, "A", True, 35.38),
    (70, "A", False, 36.0),
    (70, "A", True, 59.0),
    (0, "B", False, 6.0),
    (0, "B", True, 14.0),
    (5, "B", False, 11.5),
    (5, "B", True, 22.25),
    (19.99, "B", False, 22.99),
    (19.99, "B", True, 39.49),
    (20, "B", False, 20.0),
    (20, "B", True, 35.0),
    (70, "B", False, 55.0),
    (70, "B", True, 87.5),
    (0, "C", False, 9.5),
    (0, "C", True, 19.25),
    (5, "C", False, 17.5),
    (5, "C", True, 31.25),
    (19.99, "C", False, 35.49),
    (19.99, "C", True, 58.23),
    (20, "C", False, 30.5),
    (20, "C", True, 50.75),
    (70, "C", False, 83.0),
    (70, "C", True, 129.5),
]


@pytest.mark.parametrize("weight, zone, express, cost", RECORDED)
def test_recorded_behaviour(weight, zone, express, cost):
    assert shipping_cost(weight, zone, express) == cost


def test_unknown_zone_raises_key_error():
    with pytest.raises(KeyError):
        shipping_cost(1, "Z")


# ---- SURPRISES: recorded as-is, flagged for a human decision -------------

def test_SURPRISE_negative_weight_is_charged_the_base_fee():
    # Decision (product owner): negative weights must raise ValueError.
    # When that change is made, this test changes in the SAME commit.
    assert shipping_cost(-3, "A") == 4.5


def test_SURPRISE_exactly_20kg_uses_the_cheaper_band():
    # 20 kg is charged at the >20 kg rate, so it costs LESS than 19.99 kg.
    # Decision (product owner): this boundary is correct; keep it.
    assert shipping_cost(20, "A") < shipping_cost(19.99, "A")


def test_SURPRISE_crossing_5kg_lowers_the_price():
    # Whole-weight banding: 5.01 kg costs less than 5 kg. Not raised in the
    # book's session; found when reviewing this table. Needs a decision.
    assert shipping_cost(5.01, "A") < shipping_cost(5, "A")
