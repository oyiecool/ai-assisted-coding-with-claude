#!/usr/bin/env bash
# cleanup_tmp.sh — the ORIGINAL script being ported (scenario 7).
# Deletes regular files under DIR older than N days (find -mtime +N).
# Never follows symlinks. --dry-run lists what would be deleted, sorted.
#
# Usage: cleanup_tmp.sh [--dry-run] [--days N] DIR
set -euo pipefail

dry_run=0
days=7
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) dry_run=1; shift ;;
    --days) days="$2"; shift 2 ;;
    *) break ;;
  esac
done
dir="${1:?usage: cleanup_tmp.sh [--dry-run] [--days N] DIR}"

if [ "$dry_run" -eq 1 ]; then
  find "$dir" -type f -mtime +"$days" -print | LC_ALL=C sort
else
  find "$dir" -type f -mtime +"$days" -print -delete
fi
