# Scenario 11 — First real project with a tutor

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A learner in weeks 3–4 of the plan in section 15.8 builds a command-line expense tracker that reads a CSV file and reports spending by category and month.

**The brief**

```text
I am learning Python. Act as a tutor: hints and questions first; show
code only if I ask twice. Project: expenses.py reads a CSV with columns
date, category, amount, and prints totals per category and per month.
Help me plan it as 4 small steps. After each step, review my code and
ask me one question that checks I understand it.
```

**How the session runs**

1. Claude helps you split the work into four steps: read the CSV, total by category, total by month, and handle bad rows.
2. You write each step yourself, then ask for a review.
3. Claude asks questions such as: "What happens if the amount column is empty?" and "Why did you choose a dictionary here?"
4. When you are stuck on the month grouping, you get a hint about `date[:7]` before any code.
5. The last step adds `pytest` tests that you write, with Claude reviewing whether they would catch a broken total.

**Verify before you trust it.** You can rebuild the program from memory the next day, and your tests fail when you deliberately break the totals.

**Watch out for** asking for "the whole thing" when you are tired. Stop for the day instead.

## Files and how to run them

`expenses.csv` is sample data, including two bad rows on purpose. `solution/` holds a reference solution with tests. **Write your own version first**, then compare.

```bash
python scenarios/11-learner-expense-tracker/solution/expenses.py scenarios/11-learner-expense-tracker/expenses.csv
pytest scenarios/11-learner-expense-tracker
```
