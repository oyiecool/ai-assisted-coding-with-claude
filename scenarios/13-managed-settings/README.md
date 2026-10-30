# Scenario 13 — Roll out guard-rails to every developer

From Chapter 18 of *AI-Assisted Coding with Claude*.

**Who and goal.** An engineering lead or governance owner must make a minimum set of controls apply to every Claude Code user in the organisation, without slowing teams down.

**How the session runs**

1. Draft the non-negotiables with security: deny reads of secret files, deny network tools and destructive commands, and disable unattended permission modes.
2. Ask Claude to write the managed settings file and a one-page explainer for developers. Check every key against the current settings documentation, because settings evolve.
3. Pilot on two teams for two weeks. Collect every blocked action and decide whether each block was right.
4. Deploy through your device-management tool to the managed-settings location for each operating system, as described in the documentation.
5. Announce it with the reasons, how to request an exception, and who owns the policy.

**Verify before you trust it.** On a managed laptop, try each denied action and confirm that it is blocked and cannot be overridden in user or project settings.

**Watch out for** deny lists so broad that developers work around them with unmanaged tools. Controls that people avoid reduce safety.

## Files and how to run them

`managed-settings.json` is an example organisation-wide policy. `ROLLOUT-CHECKLIST.md` covers the pilot, deployment and measurement. Verify every settings key against the current Claude Code documentation before deploying.
