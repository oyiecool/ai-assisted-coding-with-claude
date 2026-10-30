#!/usr/bin/env python3
"""Generate scenarios/NN-*/README.md from Chapter 18 of the manuscript.

Usage: python tools/make_scenario_readmes.py MANUSCRIPT.md

Each README contains the scenario text from the book plus a "Files and how
to run them" section defined below. Re-run it when the chapter changes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RUN = {
    1: ("01-safe-csv-export", "`safe_csv.py` streams a CSV export and neutralises CSV injection. "
        "`test_safe_csv.py` covers the injection cases and a 100,000-row export.",
        "pytest scenarios/01-safe-csv-export"),
    2: ("02-rounding-bug", "`totals_buggy.py` is the original float-based total. `totals.py` "
        "implements finance's rule with `Decimal`. `test_totals.py` reproduces the five reported "
        "invoices and shows why rounding only the total is not the fix.",
        "pytest scenarios/02-rounding-bug"),
    3: ("03-onboarding", "`questions.md` is the orientation question list. "
        "`ONBOARDING-template.md` is the document the session produces.", None),
    4: ("04-dependency-remediation", "`group_findings.py` turns pip-audit JSON from several "
        "services into the smallest set of safe upgrades. `sample-audits/` contains illustrative "
        "input; its finding IDs are examples, not advice about current versions.",
        "pip-audit --format json > billing.json   # once per service\n"
        "python scenarios/04-dependency-remediation/group_findings.py "
        "scenarios/04-dependency-remediation/sample-audits/*.json\n"
        "pytest scenarios/04-dependency-remediation"),
    5: ("05-characterisation-tests", "`legacy_shipping.py` is the untested legacy function, "
        "kept exactly as found. `test_characterisation.py` records its behaviour and flags "
        "surprises separately.",
        "pytest scenarios/05-characterisation-tests\n"
        "# Then change one rate in RATES and watch the tests fail."),
    6: ("06-infra-plan-only", "`check_plan.py` fails a Terraform plan that updates, replaces or "
        "deletes anything not explicitly allowed.",
        "terraform plan -out=tfplan && terraform show -json tfplan > plan.json\n"
        "python scenarios/06-infra-plan-only/check_plan.py plan.json\n"
        "pytest scenarios/06-infra-plan-only"),
    7: ("07-bash-to-python", "`cleanup_tmp.sh` is the original script and `cleanup_tmp.py` is "
        "the port. `test_cleanup_differential.py` runs both on the same tree and compares their "
        "output.",
        "pytest scenarios/07-bash-to-python"),
    8: ("08-runbook", "`RUNBOOK-template.md` is the template, with [CHANGE] and [APPROVAL] "
        "markers and rollback steps.", None),
    9: ("09-pr-review", "`orders.py` contains the pagination change as submitted and as fixed "
        "after review, on SQLite. `test_orders.py` turns each review finding into a test and "
        "shows that the submitted version fails it.",
        "pytest scenarios/09-pr-review"),
    10: ("10-ai-review-ci", "The workflow template is in "
         "[`examples/ci/ai-review.yml`](../../examples/ci/ai-review.yml).", None),
    11: ("11-learner-expense-tracker", "`expenses.csv` is sample data, including two bad rows on "
         "purpose. `solution/` holds a reference solution with tests. **Write your own version "
         "first**, then compare.",
         "python scenarios/11-learner-expense-tracker/solution/expenses.py "
         "scenarios/11-learner-expense-tracker/expenses.csv\n"
         "pytest scenarios/11-learner-expense-tracker"),
    12: ("12-understand-an-error", "The buggy and fixed word counters and their tests are in "
         "[`examples/ch15-count-words/`](../../examples/ch15-count-words/).",
         "pytest examples/ch15-count-words"),
    13: ("13-managed-settings", "`managed-settings.json` is an example organisation-wide policy. "
         "`ROLLOUT-CHECKLIST.md` covers the pilot, deployment and measurement. Verify every "
         "settings key against the current Claude Code documentation before deploying.", None),
    14: ("14-emergency-hotfix", "No code. The hotfix checklist below is the deliverable.", None),
    15: ("15-adoption-metrics", "`ai_metrics.py` compares AI-assisted and other PRs within size "
         "buckets. `sample-prs.csv` is **synthetic** data, generated to show why the overall "
         "comparison misleads.",
         "python scenarios/15-adoption-metrics/ai_metrics.py "
         "scenarios/15-adoption-metrics/sample-prs.csv\n"
         "pytest scenarios/15-adoption-metrics"),
}

EXTRA = {
    14: """
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
""",
}


def scenario_sections(text: str) -> dict[int, tuple[str, str]]:
    sections, current, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^#### Scenario (\d+) — (.+)$", line)
        if m:
            if current:
                sections[current[0]] = (current[1], "\n".join(buf).strip())
            current, buf = (int(m.group(1)), m.group(2)), []
            continue
        if current and (line.startswith("### ") or line.startswith("## ")):
            sections[current[0]] = (current[1], "\n".join(buf).strip())
            current, buf = None, []
            continue
        if current:
            buf.append(line)
    if current:
        sections[current[0]] = (current[1], "\n".join(buf).strip())
    return sections


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    sections = scenario_sections(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for number, (folder, files, run) in RUN.items():
        title, body = sections[number]
        body = re.sub(r"\n\*\*Companion code:\*\*.*", "", body).strip()
        out = [f"# Scenario {number} — {title}", "",
               "From Chapter 18 of *AI-Assisted Coding with Claude*.", "", body, "",
               "## Files and how to run them", "", files]
        if run:
            out += ["", "```bash", run, "```"]
        if number in EXTRA:
            out.append(EXTRA[number].rstrip())
        path = ROOT / "scenarios" / folder / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
