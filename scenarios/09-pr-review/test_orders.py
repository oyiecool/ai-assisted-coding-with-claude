"""Review findings, each turned into a test (scenario 9).

Every test passes against `list_orders` (after review). The
`test_submitted_version_*` tests prove that the same checks FAIL against
the draft as submitted, which is what makes them worth adding.
"""
import sqlite3

import pytest
from orders import MAX_PAGE_SIZE, list_orders, list_orders_as_submitted

ALICE, BOB = 1, 2


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER,
                 created_at TEXT, status TEXT, total TEXT, internal_risk_score REAL)""")
    rows = []
    for i in range(1, 8):  # Alice: 7 orders, two sharing a timestamp
        stamp = "2026-10-01T10:00:00" if i in (3, 4) else f"2026-10-0{i}T09:00:00"
        rows.append((i, ALICE, stamp, "paid", f"{i}0.00", 0.1))
    rows.append((100, BOB, "2026-10-09T09:00:00", "paid", "999.00", 0.9))
    c.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", rows)
    return c


def all_ids(fetch, conn, customer, size):
    ids, page = [], 1
    while True:
        result = fetch(conn, customer, page=page, size=size)
        ids += [item["id"] for item in result["items"]]
        if not result["items"] or not result.get("has_next", len(result["items"]) == size):
            return ids
        page += 1


# ---- Finding 1: authorisation -------------------------------------------

def test_customer_cannot_page_through_other_customers_orders(conn):
    ids = all_ids(list_orders, conn, ALICE, size=3)
    assert 100 not in ids
    assert sorted(ids) == list(range(1, 8))


def test_submitted_version_leaks_other_customers_orders(conn):
    ids = all_ids(list_orders_as_submitted, conn, ALICE, size=3)
    assert 100 in ids   # the bug the reviewer caught


# ---- Findings 2 and 3: bounds --------------------------------------------

@pytest.mark.parametrize("page, size", [(0, 10), (-1, 10), (1, 0), (1, MAX_PAGE_SIZE + 1)])
def test_out_of_range_values_rejected(conn, page, size):
    with pytest.raises(ValueError):
        list_orders(conn, ALICE, page=page, size=size)


def test_submitted_version_accepts_page_zero(conn):
    list_orders_as_submitted(conn, ALICE, page=0, size=10)   # no error: the bug


# ---- Finding 4: stable ordering ------------------------------------------

def test_every_order_appears_exactly_once_across_pages(conn):
    for size in (1, 2, 3, 4):
        ids = all_ids(list_orders, conn, ALICE, size)
        assert len(ids) == len(set(ids)) == 7


def test_has_next(conn):
    assert list_orders(conn, ALICE, page=1, size=7)["has_next"] is False
    assert list_orders(conn, ALICE, page=1, size=6)["has_next"] is True


# ---- Finding 5: over-fetching --------------------------------------------

def test_internal_columns_not_exposed(conn):
    item = list_orders(conn, ALICE)["items"][0]
    assert set(item) == {"id", "created_at", "status", "total"}


def test_submitted_version_exposes_internal_columns(conn):
    assert "internal_risk_score" in list_orders_as_submitted(conn, ALICE)["items"][0]
