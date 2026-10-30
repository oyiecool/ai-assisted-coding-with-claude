#!/usr/bin/env python3
"""Fail a Terraform plan that changes more than it should (scenario 6).

Usage:
    terraform plan -out=tfplan
    terraform show -json tfplan > plan.json
    python check_plan.py plan.json [--allow ADDRESS ...] [--allow-update ADDRESS ...]

By default a plan may only CREATE resources (and read data sources). Any
update, replace or delete fails the check, unless that resource address is
explicitly allowed. This turns "touch nothing else" from a promise in a
prompt into an automatic gate.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

SAFE = {("no-op",), ("read",), ("create",)}


def classify(actions: list[str]) -> str:
    actions_t = tuple(actions)
    if actions_t in {("delete", "create"), ("create", "delete")}:
        return "replace"
    if actions_t == ("update",):
        return "update"
    if actions_t == ("delete",):
        return "delete"
    if actions_t in SAFE:
        return actions_t[0]
    return "+".join(actions_t)


def check(plan: dict, allow: set[str], allow_update: set[str]) -> tuple[Counter, list[str]]:
    counts: Counter = Counter()
    violations = []
    for change in plan.get("resource_changes", []):
        address = change["address"]
        kind = classify(change["change"]["actions"])
        counts[kind] += 1
        if kind in {"create", "no-op", "read"}:
            continue
        if address in allow:
            continue
        if kind == "update" and address in allow_update:
            continue
        violations.append(f"{kind:8} {address}")
    return counts, violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plan_json", type=Path)
    parser.add_argument("--allow", action="append", default=[],
                        help="resource address allowed any change (repeatable)")
    parser.add_argument("--allow-update", action="append", default=[],
                        help="resource address allowed an in-place update only (repeatable)")
    args = parser.parse_args(argv)
    try:
        plan = json.loads(args.plan_json.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"check_plan: cannot read plan: {exc}", file=sys.stderr)
        return 2
    if "resource_changes" not in plan:
        print("check_plan: no resource_changes in plan; is this `terraform show -json` output?",
              file=sys.stderr)
        return 2
    counts, violations = check(plan, set(args.allow), set(args.allow_update))
    summary = ", ".join(f"{n} {k}" for k, n in sorted(counts.items())) or "no changes"
    print(f"Plan: {summary}")
    if violations:
        print("NOT ALLOWED:")
        for line in violations:
            print(f"  {line}")
        return 1
    print("OK: plan only creates resources (or changes allowed addresses).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
