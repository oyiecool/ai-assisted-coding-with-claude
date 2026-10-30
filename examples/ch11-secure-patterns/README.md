# Insecure patterns and fixes — Chapter 11, section 11.7

Patterns reviewers often find in generated code, each next to its fix:

| Pattern | Vulnerable | Fixed |
| --- | --- | --- |
| SQL built from strings | `find_user_vulnerable` | `find_user` (parameterised) |
| Shell commands built from input | `archive_command_vulnerable` | `make_archive` (argument list, no shell) |
| Path traversal | `read_report_vulnerable` | `read_report` (resolve and contain) |
| Weak randomness for secrets | — | `make_token` (`secrets`) |

The tests prove both halves: the vulnerable version really is exploitable,
and the fixed version is not. The vulnerable functions are for teaching
only; never copy them into real code.

```bash
pytest examples/ch11-secure-patterns
```
