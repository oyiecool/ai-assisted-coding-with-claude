# Guard-rail rollout checklist (scenario 13)

## Decide
- [ ] Non-negotiables agreed with security (secret files, network tools,
      destructive commands, unattended modes).
- [ ] Each deny rule has a one-line reason, written down for the explainer.
- [ ] Policy owner named. Exception process defined: who approves, how
      long an exception lasts, and where it is recorded.

## Build
- [ ] `managed-settings.json` drafted. **Every key checked against the
      current Claude Code settings documentation**, because keys and rule
      syntax evolve.
- [ ] One-page explainer for developers: what is blocked, why, and how to
      ask for an exception.

## Pilot (two teams, two weeks)
- [ ] Settings deployed to pilot machines.
- [ ] On a managed laptop, each denied action tried and confirmed blocked.
- [ ] Confirmed that user and project settings cannot override the rules.
- [ ] Every block during the pilot logged and reviewed: right, or too broad?
- [ ] Rules adjusted, with the reasons recorded.

## Deploy
- [ ] Pushed through device management to the managed-settings location
      for each operating system, as given in the documentation.
- [ ] Announcement sent: the reasons, the explainer, the exception route
      and the owner.

## Measure (monthly)
- [ ] Deny-rule hits by rule and team. A rising trend is worth a look:
      it can mean injection attempts or a broken workflow.
- [ ] Exceptions granted and their age.
- [ ] Developer feedback: are people working around the controls with
      unmanaged tools?
