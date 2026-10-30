# parse_duration — Chapter 9, sections 9.1, 9.6 and 9.7

The test-first example. The order of work in the book is:

1. Write the specification.
2. Write the tests (`test_duration.py`) and review them. Reviewing them raised
   two questions the specification had not answered: are decimals allowed, and
   is whitespace allowed? Both answers were "no".
3. Commit the tests, failing.
4. Ask Claude to make them pass **without changing the tests**.

`test_duration.py` also includes the property-based tests from section 9.7,
using Hypothesis.

```bash
pytest examples/ch09-duration
```

Try mutation testing by hand: change `"m": 60` to `"m": 61` in `duration.py`
and confirm the tests fail.
