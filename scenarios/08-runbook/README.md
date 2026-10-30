# Scenario 8 — Write and verify an operations runbook

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** An SRE wants a runbook for renewing TLS certificates that a tired colleague can follow at 3 a.m.

**The brief**

```text
Draft RUNBOOK-tls-renewal.md using docs/runbook-template.md.
Sources: our cert inventory (certs.yml), certwatch (tools/certwatch),
the deploy script and last year's renewal ticket (attached).
Rules: every command must be copy-pasteable and must exist in this
repo or on our standard image. Mark steps that change production with
[CHANGE] and steps needing approval with [APPROVAL]. Include rollback.
```

**How the session runs.** Claude drafts from the real scripts. You then execute every command in staging, in order, and correct each one that is wrong. Commonly a flag has the wrong name, or a step quietly assumes access the on-call engineer does not have. A colleague who did not write it does a dry walk-through.

**Verify before you trust it.** Every command has been run at least once and every `[CHANGE]` step has a rollback step.

**Watch out for** plausible commands that do not exist, and runbooks that work only for the person who wrote them.

## Files and how to run them

`RUNBOOK-template.md` is the template, with [CHANGE] and [APPROVAL] markers and rollback steps.
