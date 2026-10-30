# Scenario 4 — Remediate a vulnerable dependency across services

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A vulnerability remediation engineer receives scanner findings for three Python services. The goal is to fix every finding with the smallest safe upgrade, with evidence.

**The brief**

```text
Attached: pip-audit JSON for services billing, search and portal.
1. Group findings by package. For each package, give the lowest
   version that fixes ALL its findings (not the latest version).
2. For each service, list the upgrades needed and check our code for
   APIs that changed between the installed and target versions, using
   the official changelog. Cite the changelog entries.
3. Propose one branch per service. Do not change anything yet.
```

**How the session runs**

1. Claude runs a small grouping script, which is in the companion code. It turns forty findings into six package upgrades.
2. **Human checkpoint.** You approve the target versions and the order: the internet-facing portal first.
3. Per service: Claude bumps the versions in the lockfile, runs the tests and fixes the API changes. Then it re-runs `pip-audit`.
4. Each branch goes through normal review and change management (Chapter 13).

**Verify before you trust it.** The rescan shows the findings closed and no new ones. The tests pass, and the staging deployment is healthy. The ticket records the before-and-after scans.

**Watch out for** upgrading to the latest major version when a patch release fixes the issue, missing a vulnerable transitive dependency, and closing tickets because the version number looks right without rescanning.

## Files and how to run them

`group_findings.py` turns pip-audit JSON from several services into the smallest set of safe upgrades. `sample-audits/` contains illustrative input; its finding IDs are examples, not advice about current versions.

```bash
pip-audit --format json > billing.json   # once per service
python scenarios/04-dependency-remediation/group_findings.py scenarios/04-dependency-remediation/sample-audits/*.json
pytest scenarios/04-dependency-remediation
```
