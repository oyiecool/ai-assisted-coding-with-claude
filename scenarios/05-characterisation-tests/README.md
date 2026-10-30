# Scenario 5 — Put a safety net under legacy code

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** A developer must change a ten-year-old shipping-cost function that has no tests and that nobody fully understands.

**The brief**

```text
Write characterisation tests for shipping_cost() in legacy/shipping.py.
Record what it returns TODAY for a wide table of inputs: weights from
0 to 70 kg including boundaries, every zone, express on and off, and
invalid values (negative weight, unknown zone).
Do not change shipping.py. List any results that look like bugs
separately so a human can decide.
```

**How the session runs.** Claude writes a parametrised test table of about forty cases that all pass against the current code. It flags two surprises: a negative weight is charged the base fee, and exactly 20 kg falls into the cheaper band. **Human checkpoint:** the product owner decides that negative weights must raise an error and that the 20 kg boundary is correct. Only after that decision do you change the code, together with the one test that changes because of it.

**Verify before you trust it.** Break the function on purpose, for example by changing one rate, and check that at least one test fails.

**Watch out for** an agent that "fixes" the surprising behaviour while writing the tests. Characterisation tests record behaviour; they do not change it.

## Files and how to run them

`legacy_shipping.py` is the untested legacy function, kept exactly as found. `test_characterisation.py` records its behaviour and flags surprises separately.

```bash
pytest scenarios/05-characterisation-tests
# Then change one rate in RATES and watch the tests fail.
```
