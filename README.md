# AI-Assisted Coding with Claude — companion code

Code, scripts and templates for the book **_AI-Assisted Coding with Claude:
A practical guide for developers, learners and the leaders who govern them_**
by Ronald Allan V. Tomimbang.

Every code listing in the book is here. So are runnable, tested versions of
the book's examples, the code for the fifteen scenarios in Chapter 18 and the
scripts that typeset the book. The examples follow the book's own rule:
nothing counts as done until it has run.

## What is where

| Folder | Contents |
| --- | --- |
| [`listings/`](listings/) | Every code block printed in the book, exactly as printed, by chapter, with an [index](listings/README.md). Many are prompts or excerpts rather than complete programs. |
| [`examples/`](examples/) | Runnable, tested versions of the chapter examples. |
| [`scenarios/`](scenarios/) | The fifteen Chapter 18 scenarios: each has its brief and walkthrough, plus tested code or templates where the scenario produces them. |
| [`templates/`](templates/) | The CLAUDE.md template, the PR "AI assistance" section and a change-record example (Appendix B, Chapter 13). |
| [`book/`](book/) | The typesetting pipeline that builds the PDF with covers (pandoc, XeLaTeX, TikZ figures). |
| [`tools/`](tools/) | Scripts that regenerate `listings/` and the scenario READMEs from the manuscript. |

### Examples by chapter

| Example | Chapter | What it shows |
| --- | --- | --- |
| [`ch01-compress-logs`](examples/ch01-compress-logs/) | 1.5 | The first brief, turned into a tested script |
| [`ch03-pr-summary`](examples/ch03-pr-summary/) | 3.11 | A small internal tool on the Claude API, tested with a fake client |
| [`claude-config`](examples/claude-config/) | 3, 4, 7 | CLAUDE.md, settings, hooks, a skill and a subagent, with hook tests |
| [`ch06-certwatch`](examples/ch06-certwatch/) | 6.7 | The core loop's worked example: a TLS expiry checker |
| [`ci`](examples/ci/) | 7.13 | A read-only AI review workflow template |
| [`ch09-duration`](examples/ch09-duration/) | 9.1, 9.6, 9.7 | Test-first development, plus property-based tests |
| [`ch09-rotate-logs`](examples/ch09-rotate-logs/) | 9.10 | A shell script tested with Bats |
| [`ch11-secure-patterns`](examples/ch11-secure-patterns/) | 11.7 | Insecure patterns next to their fixes, with tests proving the fixes |
| [`ch15-count-words`](examples/ch15-count-words/) | 15.7 | The learner's bug and the tests that catch it |

### Scenarios (Chapter 18)

| # | Scenario | Code |
| --- | --- | --- |
| 1 | [Ship a feature safely: CSV export](scenarios/01-safe-csv-export/) | `safe_csv.py` + tests |
| 2 | [Fix a production bug: invoices one cent off](scenarios/02-rounding-bug/) | buggy and fixed totals + tests |
| 3 | [Get productive in an unfamiliar repository](scenarios/03-onboarding/) | questions and template |
| 4 | [Remediate a vulnerable dependency](scenarios/04-dependency-remediation/) | `group_findings.py` + tests |
| 5 | [Put a safety net under legacy code](scenarios/05-characterisation-tests/) | characterisation tests |
| 6 | [Propose an infrastructure change, plan only](scenarios/06-infra-plan-only/) | `check_plan.py` + tests |
| 7 | [Port a fragile shell script to Python](scenarios/07-bash-to-python/) | differential tests |
| 8 | [Write and verify a runbook](scenarios/08-runbook/) | template |
| 9 | [Review a teammate's AI-assisted PR](scenarios/09-pr-review/) | review findings as tests |
| 10 | [Add AI review to CI](scenarios/10-ai-review-ci/) | workflow template |
| 11 | [First real project with a tutor](scenarios/11-learner-expense-tracker/) | exercise + reference solution |
| 12 | [Understand an error instead of pasting a fix](scenarios/12-understand-an-error/) | see `examples/ch15-count-words` |
| 13 | [Roll out guard-rails to every developer](scenarios/13-managed-settings/) | managed settings + checklist |
| 14 | [Emergency hotfix during an incident](scenarios/14-emergency-hotfix/) | checklist |
| 15 | [Measure whether AI-assisted coding works](scenarios/15-adoption-metrics/) | `ai_metrics.py` + tests |

## Run the tests

You need Python 3.11 or later. For the shell tests you also need Bats,
ShellCheck and jq.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                      # all Python tests
ruff check .                # lint
bats examples/ch09-rotate-logs examples/claude-config   # shell tests
shellcheck examples/**/*.sh scenarios/**/*.sh
```

The same checks run in GitHub Actions on every push and pull request
(`.github/workflows/tests.yml`).

## A note on accuracy

Claude Code's settings keys, permission-rule syntax, hook events and CLI
flags change over time. The configuration files here match the
documentation as of October 2026. Check them against
[code.claude.com/docs](https://code.claude.com/docs) before you rely on
them. Model names in the API example may also need updating.

Sample data is illustrative. The vulnerability findings in scenario 4 are
examples, not advice about which versions are currently safe, and the pull
request data in scenario 15 is synthetic.

## About the book

The manuscript is not in this repository. `book/` contains the build
pipeline only; see [`book/README.md`](book/README.md).
