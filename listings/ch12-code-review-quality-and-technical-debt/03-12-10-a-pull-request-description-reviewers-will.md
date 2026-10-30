## Add pagination to GET /orders (#981)

### Why
Large customers have 50k+ orders; the endpoint times out. Pagination
keeps responses under 200 ms at p95 (measured in staging).

### What changed
- `list_orders` accepts `page` (>=1) and `size` (1-200, default 50).
- Reuses `orders_for_customer()` so the customer filter is unchanged.
- Stable ordering: `created_at DESC, id DESC`.
- Response adds `page`, `size`, `has_next`; existing `items` shape kept.

### How it was tested
- New unit tests: bounds, empty result, stable ordering across pages.
- New authz test: user A cannot page through user B's orders.
- `make check` green; staging load test at 2x peak.

### AI assistance
- Plan and first draft by Claude Code. First draft rewrote the query
  and dropped the customer filter; caught in self-review and fixed.
- All code reviewed and understood by me.

### Reviewers, please check hardest
- The authorisation test (tests/api/test_orders_authz.py).
- Whether size cap 200 is right for the mobile client.
