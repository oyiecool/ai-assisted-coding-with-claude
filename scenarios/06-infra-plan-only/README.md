# Scenario 6 — Propose an infrastructure change without touching production

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A platform engineer needs a new encrypted storage bucket. The agent may write and plan the Terraform, but a human applies it.

**The brief.** Use the infrastructure brief from section 5.11, and add one line: *"Save the plan as JSON with `terraform show -json tfplan > plan.json` and run `check_plan.py` on it."*

**How the session runs**

1. Claude writes the resource following the existing bucket pattern, then runs `fmt`, `validate` and `plan`.
2. `check_plan.py` reads the plan JSON. It fails if any resource would be updated, replaced or destroyed, unless that address is on an explicit allow-list. This makes "touch nothing else" an automatic check instead of a promise.
3. **Human checkpoint.** You read the plan, a second engineer approves the change, and a pipeline you control runs `apply`.

**Verify before you trust it.** The plan shows one create and zero updates or deletes. Policy-as-code checks pass (encryption, no public access, tags), and the bucket's settings in the cloud console match the brief.

**Watch out for** credentials. If the agent's shell can reach production credentials, "plan only" is a request, not a control. Give it a role that can plan but not apply.

## Files and how to run them

`check_plan.py` fails a Terraform plan that updates, replaces or deletes anything not explicitly allowed.

```bash
terraform plan -out=tfplan && terraform show -json tfplan > plan.json
python scenarios/06-infra-plan-only/check_plan.py plan.json
pytest scenarios/06-infra-plan-only
```
