"""certwatch: report TLS certificate expiry for a list of hosts.

Exit status: 0 when every certificate is valid for more than --days days,
1 when any certificate expires within --days or any host fails, 2 on usage
errors. The tool only reads certificates; it never sends application data.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .parse import parse_hosts
from .probe import Connector, ProbeResult, probe, tls_connect

MAX_WORKERS = 16


def non_negative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("must be zero or more")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="certwatch", description=__doc__.splitlines()[0])
    parser.add_argument("hosts_file", type=Path, help="file with one host[:port] per line")
    parser.add_argument("--days", type=non_negative_int, default=21,
                        help="warn when a certificate expires within this many days (default 21)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--timeout", type=float, default=5.0, help="connect timeout in seconds")
    parser.add_argument("--no-verify", action="store_true",
                        help="read certificates without validating them (to inspect expired or "
                             "self-signed certificates); verification is on by default")
    return parser


def status(result: ProbeResult, days: int) -> str:
    if not result.ok:
        return "ERROR"
    return "EXPIRING" if result.days_left is not None and result.days_left <= days else "OK"


def render_table(results: list[ProbeResult], days: int) -> str:
    rows = [("HOST", "STATUS", "DAYS", "EXPIRES (UTC)", "SUBJECT / ERROR")]
    for r in results:
        expires = r.not_after.strftime("%Y-%m-%d") if r.not_after else "-"
        detail = r.error or r.subject
        rows.append((str(r.target), status(r, days), str(r.days_left if r.ok else "-"), expires, detail))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = []
    for row in rows:
        cells = [row[i].ljust(widths[i]) for i in range(4)] + [row[4]]
        lines.append("  ".join(cells).rstrip())
    return "\n".join(lines)


def render_json(results: list[ProbeResult], days: int) -> str:
    return json.dumps(
        [
            {
                "host": r.target.host,
                "port": r.target.port,
                "status": status(r, days),
                "days_left": r.days_left,
                "not_after": r.not_after.isoformat() if r.not_after else None,
                "subject": r.subject,
                "issuer": r.issuer,
                "error": r.error or None,
            }
            for r in results
        ],
        indent=2,
    )


def main(argv: list[str] | None = None, connect: Connector = tls_connect) -> int:
    args = build_parser().parse_args(argv)
    try:
        targets = parse_hosts(args.hosts_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"certwatch: {exc}", file=sys.stderr)
        return 2
    verify = not args.no_verify
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, max(1, len(targets)))) as pool:
        results = list(pool.map(lambda t: probe(t, args.timeout, verify, connect), targets))
    print(render_json(results, args.days) if args.json else render_table(results, args.days))
    return 1 if any(status(r, args.days) != "OK" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
