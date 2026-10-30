#!/usr/bin/env python3
"""Compress .log files older than N days in a directory (Chapter 1, 1.5).

The brief from the book:
- Python 3.11+, standard library only
- skip files that are already .gz
- --dry-run only prints what would happen
- log each action; exit non-zero if any file fails

Decisions made when Claude asked about the ambiguous parts:
- "older than N days" uses the modification time.
- The original file is removed only after the .gz is fully written.
- Only the top level of the directory is processed (no recursion).
"""
from __future__ import annotations

import argparse
import gzip
import logging
import os
import shutil
import sys
import time
from pathlib import Path

log = logging.getLogger("compress_logs")


def candidates(directory: Path, days: int, now: float | None = None) -> list[Path]:
    """Return .log files in directory whose mtime is more than `days` old."""
    cutoff = (now if now is not None else time.time()) - days * 86400
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and not p.is_symlink() and p.suffix == ".log" and p.stat().st_mtime < cutoff
    )


def compress(path: Path) -> Path:
    """gzip path to path.gz, preserving mtime, then remove the original."""
    target = path.with_name(path.name + ".gz")
    if target.exists():
        raise FileExistsError(f"{target} already exists")
    partial = target.with_name(target.name + ".partial")
    try:
        with path.open("rb") as src, gzip.open(partial, "wb") as dst:
            shutil.copyfileobj(src, dst)
        partial.rename(target)
    finally:
        partial.unlink(missing_ok=True)
    stat = path.stat()
    os.utime(target, (stat.st_atime, stat.st_mtime))
    path.unlink()
    return target


def run(directory: Path, days: int = 30, dry_run: bool = False) -> int:
    if not directory.is_dir():
        log.error("not a directory: %s", directory)
        return 2
    failures = 0
    for path in candidates(directory, days):
        if dry_run:
            log.info("would compress %s", path)
            continue
        try:
            target = compress(path)
            log.info("compressed %s -> %s", path, target.name)
        except OSError as exc:
            failures += 1
            log.error("failed %s: %s", path, exc)
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("directory", type=Path)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return run(args.directory, args.days, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
