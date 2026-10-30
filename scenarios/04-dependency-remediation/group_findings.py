#!/usr/bin/env python3
"""Group pip-audit findings into the smallest set of safe upgrades (scenario 4).

Usage:
    python group_findings.py billing.json search.json portal.json [--json]

Each argument is the JSON output of `pip-audit --format json` for one
service; the service name is taken from the file name. For every package,
the script works out the LOWEST version that fixes ALL its findings for each
service, not the latest release. This is the "minimal safe upgrade" from
Chapter 11, section 11.8.

Findings with no published fix are listed separately. They need a
different decision: mitigate, replace the package, or accept the risk with
an approved exception.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from packaging.version import InvalidVersion, Version


@dataclass
class Upgrade:
    package: str
    installed: str
    target: str | None            # None = no fix available for at least one finding
    services: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    unfixed: list[str] = field(default_factory=list)


def load(path: Path) -> list[dict]:
    """Return the dependency list from either pip-audit JSON layout."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["dependencies"] if isinstance(data, dict) else data


def finding_label(vuln: dict) -> str:
    """Prefer a CVE alias, which is what tickets and scanners usually show."""
    cves = [a for a in vuln.get("aliases", []) if a.startswith("CVE-")]
    return cves[0] if cves else vuln["id"]


def minimal_fix(installed: str, fix_versions: list[str]) -> Version | None:
    """Lowest fix version above the installed one, or None if there is none."""
    current = Version(installed)
    candidates = []
    for text in fix_versions:
        try:
            version = Version(text)
        except InvalidVersion:
            continue
        if version > current:
            candidates.append(version)
    return min(candidates) if candidates else None


def plan_upgrades(audits: dict[str, list[dict]]) -> list[Upgrade]:
    """audits maps service name -> pip-audit dependency list."""
    grouped: dict[tuple[str, str], Upgrade] = {}
    for service, deps in sorted(audits.items()):
        for dep in deps:
            vulns = dep.get("vulns") or []
            if not vulns:
                continue
            name, installed = dep["name"].lower(), dep["version"]
            key = (name, installed)
            upgrade = grouped.get(key)
            if upgrade is None:
                fixes, unfixed, labels = [], [], []
                for vuln in vulns:
                    label = finding_label(vuln)
                    labels.append(label)
                    fix = minimal_fix(installed, vuln.get("fix_versions", []))
                    if fix is None:
                        unfixed.append(label)
                    else:
                        fixes.append(fix)
                target = None if unfixed else str(max(fixes))
                upgrade = grouped[key] = Upgrade(
                    name, installed, target, [], sorted(set(labels)), sorted(set(unfixed))
                )
            upgrade.services.append(service)
    return sorted(grouped.values(), key=lambda u: (u.target is not None, u.package, u.installed))


def render_table(upgrades: list[Upgrade]) -> str:
    total = sum(len(u.findings) * len(u.services) for u in upgrades)
    lines = [f"{total} findings -> {len(upgrades)} package upgrades", ""]
    for u in upgrades:
        services = ", ".join(u.services)
        if u.target:
            lines.append(f"UPGRADE  {u.package} {u.installed} -> {u.target}  [{services}]")
        else:
            lines.append(f"NO FIX   {u.package} {u.installed}  [{services}]  unfixed: {', '.join(u.unfixed)}")
        lines.append(f"         findings: {', '.join(u.findings)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("audits", nargs="+", type=Path, help="pip-audit JSON files, one per service")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    try:
        audits = {path.stem: load(path) for path in args.audits}
    except (OSError, ValueError, KeyError) as exc:
        print(f"group_findings: cannot read input: {exc}", file=sys.stderr)
        return 2
    upgrades = plan_upgrades(audits)
    if args.json:
        print(json.dumps([u.__dict__ for u in upgrades], indent=2))
    else:
        print(render_table(upgrades))
    return 1 if any(u.target is None for u in upgrades) else 0


if __name__ == "__main__":
    raise SystemExit(main())
