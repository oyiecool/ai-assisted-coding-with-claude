# Scenario 14 — Emergency hotfix during an incident

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** An on-call engineer, working with an incident commander, must stop customer-facing errors quickly without creating a second incident.

**How the session runs**

1. **Stabilise first.** Before writing any code, consider rollback, a feature flag or scaling. AI is not needed for a revert.
2. If a code fix is needed, give Claude the evidence (errors, recent deploys, the diff since the last good release) in plan mode and ask for ranked hypotheses (Chapter 8).
3. Ask for the **smallest** fix plus a regression test. Reject refactors and "while we're here" changes.
4. A second engineer reviews the diff live. The emergency-change process applies, including the record.
5. After the incident, the review covers the AI-assisted parts too: what helped, what was wrong, and what context was missing.

**Verify before you trust it.** The regression test fails before the fix and passes after it, and error rates recover in production dashboards.

**Watch out for** pressure to skip review. A wrong hotfix during an incident is the most expensive kind of change.

## Files and how to run them

No code. The hotfix checklist below is the deliverable.

## Hotfix checklist

- [ ] Stabilised first? Rollback, feature flag or scaling considered before any code.
- [ ] Evidence collected: errors, recent deploys, diff since last good release.
- [ ] Claude asked for ranked hypotheses in plan mode, not "fix it".
- [ ] Smallest possible fix, plus a regression test that fails before and passes after.
- [ ] No refactors or "while we're here" changes in the diff.
- [ ] Second engineer reviewed the diff live.
- [ ] Emergency change recorded, including that the fix was AI-assisted.
- [ ] Error rates recovered on production dashboards.
- [ ] Post-incident review covers the AI-assisted parts: what helped, what was wrong,
      what context was missing.
