# Scenario 3 — Get productive in an unfamiliar repository

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** An engineer who has just joined a team, or inherited a service, wants a reliable mental model of the code within one day.

**The brief**

```text
Work in plan mode; do not change any files except ONBOARDING.md.
1. What does this system do, for whom, and how is it deployed?
2. Main modules and their dependencies.
3. Trace one real request end to end, citing file:line.
4. How to run it locally and run the tests.
5. The riskiest or most confusing areas, and why.
Write the answers to ONBOARDING.md. Mark every claim you could not
confirm from the code as UNVERIFIED.
```

**How the session runs.** Claude explores and drafts. You then follow ONBOARDING.md literally on a clean machine, fixing every step that does not work. Next, you pick three traced claims and check them by stepping through with a debugger. Finally, a team member reviews the document.

**Verify before you trust it.** The tests run by following the document alone, and every UNVERIFIED mark is either confirmed or removed.

**Watch out for** confident descriptions of framework "magic" (dependency injection, signals, decorators) that the agent guessed rather than traced.

## Files and how to run them

`questions.md` is the orientation question list. `ONBOARDING-template.md` is the document the session produces.
