"""Expense tracker — a reference solution for scenario 11.

Open this only after you have written your own version. Yours does not have
to look like this; it has to work, and you have to be able to explain it.

Usage: python expenses.py expenses.csv
"""
import csv
import sys
from decimal import Decimal, InvalidOperation


def read_expenses(path):
    """Return (rows, problems). Bad rows are reported, not fatal."""
    rows, problems = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):  # line 1 is the header
            date = (row.get("date") or "").strip()
            category = (row.get("category") or "").strip()
            amount_text = (row.get("amount") or "").strip()
            if len(date) != 10 or date[4] != "-" or date[7] != "-":
                problems.append(f"line {line_number}: bad date {date!r}")
                continue
            if not category:
                problems.append(f"line {line_number}: missing category")
                continue
            try:
                amount = Decimal(amount_text)
            except InvalidOperation:
                problems.append(f"line {line_number}: bad amount {amount_text!r}")
                continue
            rows.append({"date": date, "category": category, "amount": amount})
    return rows, problems


def total_by(rows, key):
    totals = {}
    for row in rows:
        name = key(row)
        totals[name] = totals.get(name, Decimal("0")) + row["amount"]
    return dict(sorted(totals.items()))


def by_category(rows):
    return total_by(rows, lambda row: row["category"])


def by_month(rows):
    return total_by(rows, lambda row: row["date"][:7])   # "2026-10-03" -> "2026-10"


def report(path):
    rows, problems = read_expenses(path)
    lines = ["By category:"]
    lines += [f"  {name:<14}{amount:>10.2f}" for name, amount in by_category(rows).items()]
    lines += ["", "By month:"]
    lines += [f"  {name:<14}{amount:>10.2f}" for name, amount in by_month(rows).items()]
    if problems:
        lines += ["", f"Skipped {len(problems)} bad row(s):"] + [f"  {p}" for p in problems]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python expenses.py FILE.csv")
        sys.exit(2)
    print(report(sys.argv[1]))
