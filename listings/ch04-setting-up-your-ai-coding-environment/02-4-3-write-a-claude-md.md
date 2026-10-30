# Project: invoice-service

## Purpose
REST service that generates and stores customer invoices.

## Commands
- Setup: `uv sync`
- Tests: `uv run pytest -q`
- Lint and format: `uv run ruff check . && uv run ruff format .`
- Types: `uv run mypy src`

## Conventions
- Python 3.12, type hints everywhere, no bare `except`.
- Money is `decimal.Decimal`, never float.
- Database access only through `src/repo/`.
- New endpoints need a test in `tests/api/`.

## Do not
- Edit files in `migrations/` by hand; use `alembic revision`.
- Add dependencies without asking.
- Read or print anything from `.env`.

## Definition of done
Tests, lint and type checks pass; CHANGELOG.md updated.
