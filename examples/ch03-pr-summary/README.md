# pr_summary.py — Chapter 3, section 3.11

A small internal tool on the Claude API: it drafts a plain-English summary of
the current branch's diff for reviewers.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...        # from your CI secret store, never committed
python examples/ch03-pr-summary/pr_summary.py origin/main
```

Design choices worth copying:

- a narrow system prompt that forbids inventing behaviour;
- an input guard that refuses a very large diff instead of truncating it silently;
- the diff wrapped in `<diff>` tags and treated as data, as basic prompt-injection hygiene;
- a draft for humans, not a decision: it cannot approve or merge anything.

The tests use a fake client, so they run without the SDK or network access:

```bash
pytest examples/ch03-pr-summary
```

Before running it in CI, confirm that your organisation's agreement covers
sending source code through the API. Also check the current model names and
pricing in the API documentation; the `MODEL` constant may need updating.
