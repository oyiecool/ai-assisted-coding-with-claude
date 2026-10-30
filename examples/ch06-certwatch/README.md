# certwatch — Chapter 6, section 6.7

The worked example of the core loop: plan, generate, review, test, commit.
`certwatch` checks TLS certificate expiry for a list of hosts and exits
non-zero if any certificate expires within a threshold or any host fails.

```bash
cd examples/ch06-certwatch
printf 'example.com\nwww.python.org:443\n' > hosts.txt
python -m certwatch hosts.txt --days 21
python -m certwatch hosts.txt --json
```

| Option | Meaning |
| --- | --- |
| `--days N` | Warn when a certificate expires within N days (default 21) |
| `--json` | JSON output instead of a table |
| `--timeout S` | Connect timeout per host, in seconds (default 5) |
| `--no-verify` | Read certificates without validating them, for expired or self-signed certificates. Verification is on by default. |

Exit codes: `0` all OK, `1` something is expiring or failed, `2` usage error.

Design points from the book's review step:

- The network call is injected (`connect`), so the tests never touch the network.
- All dates are UTC.
- Verification stays on by default. `--no-verify` exists only to read
  certificates that would fail validation, and the tool never sends data.
- Hosts are checked concurrently with at most 16 threads.

Run the tests from the repository root with `pytest examples/ch06-certwatch`.
