# compress_logs.py — Chapter 1, section 1.5

The book's first brief, carried through to a tested script:

```text
Write a Python 3.11 script that compresses .log files older than 30 days
in a directory given as a CLI argument. Requirements:
- use only the standard library
- skip files that are already .gz
- dry-run flag that only prints what would happen
- log each action; exit non-zero if any file fails
Ask me anything that is ambiguous before writing code.
```

The questions Claude asked, and the answers recorded in the module docstring:
"older than" uses modification time; the original is removed only after the
`.gz` is fully written; only the top level of the directory is processed;
symlinks are ignored.

```bash
python examples/ch01-compress-logs/compress_logs.py /var/log/myapp --dry-run
pytest examples/ch01-compress-logs
```

The same task in Bash, with Bats tests, is in
[`../ch09-rotate-logs`](../ch09-rotate-logs/).
