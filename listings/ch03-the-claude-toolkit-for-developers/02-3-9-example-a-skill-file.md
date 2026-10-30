---
name: db-migration
description: Use when creating or changing database tables, columns or indexes.
---

# Writing a database migration

1. Generate a revision: `uv run alembic revision -m "<summary>"`.
2. Write both upgrade() and downgrade(). Downgrade must fully reverse upgrade.
3. Never drop a column in the same release that stops using it. Use two releases.
4. For tables over 1M rows, add indexes CONCURRENTLY and note the lock risk.
5. Run `uv run alembic upgrade head` and `downgrade -1` against the test DB.
6. Add a line to docs/migrations.md describing the change and its rollback.
