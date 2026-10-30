# Scenario 7 — Port a fragile shell script to Python

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A sysadmin wants to replace a cron-driven cleanup script written in Bash with a tested Python version that behaves identically.

**The brief**

```text
Port scripts/cleanup_tmp.sh to Python 3.12 (standard library only) as
cleanup_tmp.py with the same CLI: DIR, --days N, --dry-run.
Behaviour must be identical. First, write a differential test that
builds a temporary tree (old/new files, nested dirs, names with spaces,
a symlink), runs BOTH scripts in --dry-run, and compares the sorted
list of files each would delete. Then implement until it passes.
```

**How the session runs.** Claude explains the Bash script line by line first; you confirm that symlinks must never be followed. The differential test fails until the Python version skips symlinks and treats `-mtime +N` exactly the way `find` does: whole 24-hour periods, so a file must be *more* than N full days old. Then you add unit tests for the Python-only improvements: clear error messages and a non-zero exit code on a missing directory.

**Verify before you trust it.** Run both versions in dry-run mode on a copy of the real directory. Run the cron job with the new script in dry-run mode for a week before switching off the old one.

**Watch out for** off-by-one-day differences. `find -mtime +7` and "older than 7 days" are not the same thing, and an agent will happily assume they are.

## Files and how to run them

`cleanup_tmp.sh` is the original script and `cleanup_tmp.py` is the port. `test_cleanup_differential.py` runs both on the same tree and compares their output.

```bash
pytest scenarios/07-bash-to-python
```
