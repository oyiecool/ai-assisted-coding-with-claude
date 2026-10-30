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

## Security rules
- All SQL through the ORM or parameterised queries. Never string-format SQL.
- Validate and bound every external input (size, type, range).
- Use `secrets` for tokens; never `random`.
- Passwords: argon2id via `passlib`; never hash with MD5/SHA-1.
- No secrets in code, tests or logs. Read from the environment via `settings.py`.
- New dependencies need human approval and must be in the internal registry.

## Do not
- Edit files in `migrations/` by hand; use `alembic revision`.
- Add dependencies without asking.
- Read or print anything from `.env`.

## Definition of done
Tests, lint and type checks pass; CHANGELOG.md updated.
