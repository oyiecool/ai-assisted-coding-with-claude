"""Pagination for "list my orders" (Chapter 12, 12.7; scenario 9).

`list_orders_as_submitted` is the AI-generated first draft from the pull
request, adapted to SQLite. It is parameterised, readable and passes a basic
test, and it has five problems a careful review finds:

1. Authorisation regression: the customer filter is gone, so every
   customer's orders are returned.
2. Unbounded size: a caller can ask for a million rows.
3. Invalid page: page 0 or a negative page gives a negative offset.
4. Unstable ordering: orders with the same created_at can appear on two
   pages or on none.
5. Over-fetching: SELECT * returns internal columns.

`list_orders` is the version after review. It reuses the existing
`orders_for_customer_query`, the step the original brief should have
required.
"""
from __future__ import annotations

import sqlite3

MAX_PAGE_SIZE = 200
PUBLIC_COLUMNS = "id, created_at, status, total"


def orders_for_customer_query() -> str:
    """The existing query function the endpoint already used before the PR."""
    return f"SELECT {PUBLIC_COLUMNS} FROM orders WHERE customer_id = :customer_id"


def list_orders_as_submitted(conn: sqlite3.Connection, customer_id: int,
                             page: int = 1, size: int = 50) -> dict:
    offset = (page - 1) * size
    rows = conn.execute(
        "SELECT * FROM orders ORDER BY created_at DESC LIMIT :size OFFSET :offset",
        {"size": size, "offset": offset},
    ).fetchall()
    return {"page": page, "items": [dict(r) for r in rows]}


def list_orders(conn: sqlite3.Connection, customer_id: int,
                page: int = 1, size: int = 50) -> dict:
    if page < 1:
        raise ValueError("page must be 1 or more")
    if not 1 <= size <= MAX_PAGE_SIZE:
        raise ValueError(f"size must be between 1 and {MAX_PAGE_SIZE}")
    rows = conn.execute(
        orders_for_customer_query()
        + " ORDER BY created_at DESC, id DESC LIMIT :limit OFFSET :offset",
        {"customer_id": customer_id, "limit": size + 1, "offset": (page - 1) * size},
    ).fetchall()
    return {
        "page": page,
        "size": size,
        "has_next": len(rows) > size,
        "items": [dict(r) for r in rows[:size]],
    }
