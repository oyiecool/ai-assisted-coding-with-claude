#!/usr/bin/env bash
# rotate_logs.sh — compress .log files older than 30 days (Chapter 9, 9.10).
#
# Usage: rotate_logs.sh [--dry-run] [--days N] DIR
#
# Compresses DIR/*.log files whose modification time is more than N days
# old (default 30; same meaning as `find -mtime +N`). Skips files that are
# already .gz and never follows symlinks. Exits non-zero if DIR is missing
# or any file fails to compress.
set -euo pipefail

usage() { echo "usage: $0 [--dry-run] [--days N] DIR" >&2; exit 2; }

dry_run=0
days=30
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) dry_run=1; shift ;;
    --days) [ $# -ge 2 ] || usage; days="$2"; shift 2 ;;
    -h|--help) usage ;;
    --) shift; break ;;
    -*) usage ;;
    *) break ;;
  esac
done
[ $# -eq 1 ] || usage
dir="$1"

case "$days" in
  ''|*[!0-9]*) echo "error: --days must be a whole number" >&2; exit 2 ;;
esac
if [ ! -d "$dir" ]; then
  echo "error: not a directory: $dir" >&2
  exit 1
fi

failures=0
while IFS= read -r -d '' file; do
  if [ "$dry_run" -eq 1 ]; then
    echo "would compress $file"
    continue
  fi
  if gzip -9 -- "$file"; then
    echo "compressed $file"
  else
    echo "failed $file" >&2
    failures=$((failures + 1))
  fi
done < <(find "$dir" -maxdepth 1 -type f -name '*.log' -mtime +"$days" -print0)

[ "$failures" -eq 0 ]
