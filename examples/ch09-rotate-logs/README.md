# rotate_logs.sh — Chapter 9, section 9.10

A log-rotation script with the Bats tests from the book, plus tests for names
with spaces, symlinks and bad arguments. Every test runs in a temporary
directory; never let a test for a destructive script touch real paths.

```bash
shellcheck examples/ch09-rotate-logs/rotate_logs.sh
bats examples/ch09-rotate-logs
examples/ch09-rotate-logs/rotate_logs.sh --dry-run /var/log/myapp
```

Requires GNU `find`, `gzip` and Bash 4 or later. `--days N` has exactly the
meaning of `find -mtime +N`: the file must be more than N whole 24-hour
periods old.
