#!/usr/bin/env python3
"""Compare AI-assisted and other pull requests, size for size (scenario 15).

Usage: python ai_metrics.py prs.csv

Input CSV columns (one row per merged pull request):
    pr, merged_at, ai_assisted, lead_time_hours, lines_changed, caused_incident
where ai_assisted and caused_incident are yes/no.

Definitions (agree these with your team BEFORE looking at the results):
- lead time: hours from first commit to merge;
- change failure: the PR caused an incident or a rollback;
- size buckets: S < 100 changed lines, M 100-499, L 500 or more.

The comparison is made within each size bucket, because AI-assisted PRs are
often larger and larger PRs are slower and riskier for reasons that have
nothing to do with AI. Small groups are flagged: below MIN_GROUP pull
requests, a rate is noise, not evidence.
"""
from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from statistics import median

MIN_GROUP = 10
BUCKETS = (("S", 0, 100), ("M", 100, 500), ("L", 500, float("inf")))


@dataclass
class Group:
    count: int
    median_lead_time: float | None
    failure_rate: float | None

    @property
    def small(self) -> bool:
        return self.count < MIN_GROUP


def yes(value: str) -> bool:
    value = value.strip().lower()
    if value not in {"yes", "no", "true", "false", "1", "0"}:
        raise ValueError(f"expected yes/no, got {value!r}")
    return value in {"yes", "true", "1"}


def bucket(lines_changed: int) -> str:
    for name, low, high in BUCKETS:
        if low <= lines_changed < high:
            return name
    raise ValueError(lines_changed)


def load(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f):
            rows.append({
                "ai": yes(row["ai_assisted"]),
                "lead": float(row["lead_time_hours"]),
                "size": bucket(int(row["lines_changed"])),
                "failed": yes(row["caused_incident"]),
            })
        return rows


def summarise(rows: list[dict]) -> Group:
    if not rows:
        return Group(0, None, None)
    return Group(
        count=len(rows),
        median_lead_time=median(r["lead"] for r in rows),
        failure_rate=sum(r["failed"] for r in rows) / len(rows),
    )


def compare(rows: list[dict]) -> dict[str, dict[str, Group]]:
    table = {}
    for name, _, _ in BUCKETS:
        in_bucket = [r for r in rows if r["size"] == name]
        table[name] = {
            "ai": summarise([r for r in in_bucket if r["ai"]]),
            "other": summarise([r for r in in_bucket if not r["ai"]]),
        }
    table["all"] = {"ai": summarise([r for r in rows if r["ai"]]),
                    "other": summarise([r for r in rows if not r["ai"]])}
    return table


def fmt(group: Group) -> str:
    if group.count == 0:
        return f"{'-':>5} {'-':>9} {'-':>8}"
    flag = " *" if group.small else ""
    return (f"{group.count:>5} {group.median_lead_time:>8.1f}h "
            f"{group.failure_rate:>7.0%}{flag}")


def render(table: dict[str, dict[str, Group]]) -> str:
    lines = [f"{'Size':<5} | {'AI-assisted':^25} | {'Other':^25}",
             f"{'':<5} | " + " | ".join([f"{'PRs':>5} {'lead time':>9} {'failures':>8}"] * 2)]
    for name in ["S", "M", "L", "all"]:
        lines.append(f"{name:<5} | {fmt(table[name]['ai']):<25} | {fmt(table[name]['other'])}")
    lines.append("")
    lines.append(f"* fewer than {MIN_GROUP} PRs: treat as noise, not evidence.")
    lines.append("Compare within a size row; the 'all' row mixes sizes and can mislead.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.splitlines()[2], file=sys.stderr)
        return 2
    try:
        rows = load(argv[0])
    except (OSError, KeyError, ValueError) as exc:
        print(f"ai_metrics: cannot read input: {exc}", file=sys.stderr)
        return 2
    print(render(compare(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
