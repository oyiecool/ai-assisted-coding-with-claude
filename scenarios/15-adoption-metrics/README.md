# Scenario 15 — Measure whether AI-assisted coding works

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** An engineering manager must report to leadership whether AI-assisted work is faster without being worse (section 16.10).

**How the session runs**

1. Export merged pull requests for the last two quarters with these fields: lead time, size, an AI-assisted label, and whether the change caused an incident or rollback.
2. Ask Claude to write a small analysis script, then review its definitions: what counts as a failure, and how lead time is measured.
3. Run it, and compare labelled and unlabelled PRs of similar size, because AI-assisted PRs are often larger.
4. Present ranges and the method, not one headline number.

**Verify before you trust it.** Hand-check the figures for one week of PRs against the source system.

**Watch out for** comparing unlike work. A team that uses AI only for small fixes will look faster for reasons that have nothing to do with AI.

## Files and how to run them

`ai_metrics.py` compares AI-assisted and other PRs within size buckets. `sample-prs.csv` is **synthetic** data, generated to show why the overall comparison misleads.

```bash
python scenarios/15-adoption-metrics/ai_metrics.py scenarios/15-adoption-metrics/sample-prs.csv
pytest scenarios/15-adoption-metrics
```
