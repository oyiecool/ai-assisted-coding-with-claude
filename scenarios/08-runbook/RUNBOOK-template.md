# Runbook: <task, e.g. TLS certificate renewal>

| | |
| --- | --- |
| Owner | <team> |
| Last executed end to end | <date, by whom, in which environment> |
| Expected duration | <minutes> |
| Needs approval | <yes/no; from whom> |

Markers: **[CHANGE]** changes production. **[APPROVAL]** needs approval
before you continue. Every [CHANGE] step has a matching rollback step.

## When to use this runbook
<trigger: alert name, certwatch warning, calendar reminder>

## Before you start
- [ ] Access you need: <roles, VPN, bastion>
- [ ] Tools you need: <commands, with versions>
- [ ] Change record: <link or number>

## Steps
1. Check the current state:
   ```bash
   <command that only reads>
   ```
   Expected output: <what good looks like>
2. **[APPROVAL]** <who approves, and how>
3. **[CHANGE]** <action>
   ```bash
   <command>
   ```
   Expected output: <…>
   If this fails: go to Rollback step R1.

## Verify
```bash
<command that proves success>
```

## Rollback
- R1. <undo step 3>
  ```bash
  <command>
  ```

## After
- [ ] Update the change record with evidence.
- [ ] Note anything in this runbook that was wrong, and fix it today.
