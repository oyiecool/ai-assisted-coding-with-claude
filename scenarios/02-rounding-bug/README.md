# Scenario 2 — Fix a production bug: invoices one cent off

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A developer on call learns that about 0.3% of invoices are one cent off. The goal is to fix the cause, not the sample.

**The brief**

```text
Evidence: 5 invoices attached with expected (finance) and actual totals.
All differ by exactly 0.01. Totals are computed in src/billing/totals.py.
Task: List 3 hypotheses ranked by likelihood, with evidence for and
against each. Then write a failing test that reproduces invoice #2.
Do not change totals.py yet.
```

**How the session runs**

1. Claude ranks the hypotheses: floating-point arithmetic on money; rounding each line instead of the total, or the reverse; a rounding mode that differs from finance policy.
2. Claude writes a test with invoice #2's exact lines. It fails with 0.01 difference.
3. **Human checkpoint.** You confirm the rule with finance: amounts are `Decimal`, each line is rounded half-up to cents, and the total is the sum of rounded lines.
4. Claude rewrites the calculation with `Decimal` and `ROUND_HALF_UP`. All five sample invoices now match.

**Verify before you trust it.** Recompute last month's invoices with the old and new code. Every difference should be one of the known affected invoices, and nothing else should change.

**Watch out for** a "fix" that rounds only the final total until the five samples match. It passes the tests you have and fails the invoices you have not seen.

## Files and how to run them

`totals_buggy.py` is the original float-based total. `totals.py` implements finance's rule with `Decimal`. `test_totals.py` reproduces the five reported invoices and shows why rounding only the total is not the fix.

```bash
pytest scenarios/02-rounding-bug
```
