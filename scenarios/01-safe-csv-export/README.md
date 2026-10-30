# Scenario 1 — Ship a feature safely: CSV export

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A backend developer must add a CSV download to an existing report without opening a security hole or exhausting memory on large reports.

**The brief**

```text
Goal: Add GET /reports/{id}/export.csv for users who can view the report.
Context: Report rows come from build_report() in src/reports/service.py.
Follow the response pattern in src/reports/views.py.
Constraints:
- Reuse build_report so permissions match the on-screen report exactly.
- Stream rows; never hold the whole report in memory.
- Use the csv module. Neutralise CSV injection: prefix any cell that
  starts with =, +, -, @, tab or carriage return with a single quote.
- No new dependencies.
Done when: tests cover permissions, injection cases and a 100,000-row
export; make check is green.
Process: Propose a plan and wait for my approval.
```

**How the session runs**

1. Plan mode: Claude reads the service and views, then proposes a small `safe_cell()` helper, a streaming writer and the endpoint. You approve.
2. Tests first for `safe_cell()`: each dangerous prefix, normal text, numbers and empty cells. Commit them failing.
3. Claude implements the helper and the streaming writer until the tests pass.
4. Claude adds the endpoint and its permission test. Commit.
5. You ask the security-reviewer subagent to review the diff.

**Verify before you trust it**

- Open an exported file containing `=HYPERLINK(...)` in a spreadsheet application and confirm it shows as text.
- Watch memory while exporting 100,000 rows.
- Log in as a user without access and confirm a 403 or 404 response.

**Watch out for** an agent that hand-builds CSV strings instead of using the `csv` module, and guards that forget tab and carriage return.

## Files and how to run them

`safe_csv.py` streams a CSV export and neutralises CSV injection. `test_safe_csv.py` covers the injection cases and a 100,000-row export.

```bash
pytest scenarios/01-safe-csv-export
```
