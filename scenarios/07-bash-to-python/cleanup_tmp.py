#!/usr/bin/env python3
"""cleanup_tmp.py — the Python port of cleanup_tmp.sh (scenario 7).

Same CLI and the same behaviour, checked by a differential test:
- regular files only, at any depth; symlinks are never followed or deleted;
- "older than N days" means exactly what `find -mtime +N` means: the file's
  age in WHOLE 24-hour periods (fractions discarded) must be greater than N.
  A file 7.9 days old is NOT matched by --days 7; a file 8.0 days old is;
- --dry-run prints the matching paths, sorted, and deletes nothing.

Python-only improvements, covered by unit tests:
- a clear error and exit code 2 when DIR is missing or --days is invalid.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

DAY = 86400


def matches(directory: str, days: int, now: float | None = None) -> list[str]:
    now = time.time() if now is None else now
    found = []
    for root, _dirs, files in os.walk(directory, followlinks=False):
        for name in files:
            path = os.path.join(root, name)
            if os.path.islink(path):
                continue
            age_whole_days = int((now - os.lstat(path).st_mtime) // DAY)
            if age_whole_days > days:
                found.append(path)
    return sorted(found, key=lambda p: p.encode())  # same order as LC_ALL=C sort


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Delete files older than N days.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("dir")
    args = parser.parse_args(argv)
    if args.days < 0:
        print("cleanup_tmp: --days must be zero or more", file=sys.stderr)
        return 2
    if not os.path.isdir(args.dir):
        print(f"cleanup_tmp: not a directory: {args.dir}", file=sys.stderr)
        return 2
    for path in matches(args.dir, args.days):
        print(path)
        if not args.dry_run:
            os.remove(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
