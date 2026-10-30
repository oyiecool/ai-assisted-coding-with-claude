# Project: ai-assisted-coding-with-claude

## Purpose
Companion code for the book "AI-Assisted Coding with Claude": every code
listing, runnable examples, Chapter 18 scenario code and the book's build
pipeline.

## Commands
- Setup: `pip install -r requirements-dev.txt`
- Tests: `pytest`
- Lint: `ruff check .`
- Shell: `bats examples/ch09-rotate-logs examples/claude-config` and `shellcheck` on `*.sh`
- Regenerate listings: `python tools/extract_listings.py MANUSCRIPT.md`
- Regenerate scenario READMEs: `python tools/make_scenario_readmes.py MANUSCRIPT.md`
- Build the book: `make -C book MANUSCRIPT=/path/to/manuscript.md`

## Conventions
- Python 3.11+, standard library first; `packaging`, `pytest`, `hypothesis` and `pypdf` are the only extra dependencies.
- Each example or scenario folder is self-contained: code, `test_*.py` next to it, and a README.
- Test file names must be unique across the repository (pytest runs without packages).
- Tests never touch the network; inject the dependency instead (see `certwatch`).
- Money is `Decimal`. Times are UTC.

## Do not
- Edit anything in `listings/` by hand; it is generated from the manuscript.
- Commit the manuscript or `book/build/`.
- Put an active AI-review workflow in `.github/workflows/`; `examples/ci/ai-review.yml` is a template.

## Definition of done
`pytest`, `ruff check .`, the Bats suites and ShellCheck all pass, and the
README of the folder you changed is up to date.
