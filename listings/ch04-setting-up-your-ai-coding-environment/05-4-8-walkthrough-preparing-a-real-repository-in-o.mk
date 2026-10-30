.PHONY: setup test lint types check
setup: ; uv sync
test:  ; uv run pytest -q
lint:  ; uv run ruff check . && uv run ruff format --check .
types: ; uv run mypy src
check: lint types test
