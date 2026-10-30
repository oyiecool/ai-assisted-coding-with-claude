# Scenario 12 — Understand an error instead of pasting a fix

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A learner's word counter (section 15.7) returns zero for every file. The goal is to find the cause yourself.

**The brief**

```text
My function returns 0 for every file. Do not fix it. Ask me questions
that help me trace the loop by hand, one at a time.
```

**How the session runs.** Claude asks you to trace the loop with a two-line file. You notice that `count` is set after the loop from the last line only. You move it inside the loop with `+=`. Claude then asks for two test cases that would have caught the bug: a file whose last line is empty, and a file with several lines.

**Verify before you trust it.** You can explain in one sentence why the original code returned zero.

**Watch out for** the habit of pasting tracebacks and accepting fixes. A fix you do not understand teaches you nothing.

## Files and how to run them

The buggy and fixed word counters and their tests are in [`examples/ch15-count-words/`](../../examples/ch15-count-words/).

```bash
pytest examples/ch15-count-words
```
