# Scenario 9 — Review a teammate's AI-assisted pull request

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A reviewer receives a pagination change (section 12.7) and must decide whether to approve it.

**How the session runs**

1. Read the PR description first. If it has no brief, test evidence or AI-assistance note, ask for them before reviewing.
2. Run an AI pre-review with the read-only reviewer subagent:

```text
Review this diff against docs/review.md. Focus on authorisation, input
bounds and result ordering. Report only real issues with file:line,
severity and a failing test that would demonstrate each one.
```

3. Spend your own attention on the high-risk parts. Here that is the query: did it keep the customer filter?
4. Ask for a test for each issue you find, not just a fix. The authorisation test, "user A cannot page through user B's orders", is the one that matters most.

**Verify before you trust it.** The new tests fail on the original diff and pass on the fixed one.

**Watch out for** approving because the code looks tidy. The most dangerous bug in the example, a dropped customer filter, is invisible to style-level review.

## Files and how to run them

`orders.py` contains the pagination change as submitted and as fixed after review, on SQLite. `test_orders.py` turns each review finding into a test and shows that the submitted version fails it.

```bash
pytest scenarios/09-pr-review
```
