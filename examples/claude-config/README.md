# Claude Code configuration — Chapters 3, 4, 7 and 11

A complete example of the repository setup the book recommends. Copy what you
need into your own repository.

| File | What it is | Book |
| --- | --- | --- |
| `CLAUDE.example.md` | Project briefing Claude reads every session. Rename it to `CLAUDE.md` in your repository. | 4.3, 11.2 |
| `.claude/settings.json` | Team permissions (allow/deny) and hook registration. Commit this file. | 4.4, 7.6 |
| `.claude/hooks/protect-paths.sh` | PreToolUse hook that blocks edits to migrations, generated files, lockfiles and `.env` files | 7.11 |
| `.claude/hooks/format.sh` | PostToolUse hook that formats only the edited file | 4.5 |
| `.claude/skills/db-migration/SKILL.md` | A skill: an on-demand procedure with a trigger-style description | 3.9 |
| `.claude/agents/security-reviewer.md` | A read-only reviewer subagent | 3.10 |
| `test_protect_paths.bats` | Tests for the hook | 7.11 |

The example CLAUDE.md is named `CLAUDE.example.md` on purpose. Claude Code
loads files named `CLAUDE.md` automatically, and this one describes an
imaginary service, not this repository.

**Check against the current documentation.** Settings keys, permission-rule
syntax, hook events and their input format, and subagent frontmatter all
evolve. These files reflect the documentation at the time of writing (October
2026). Before relying on them, verify them at
[code.claude.com/docs](https://code.claude.com/docs).

Hooks need `jq`. Run the hook tests with:

```bash
bats examples/claude-config/test_protect_paths.bats
```
