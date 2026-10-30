## Security rules
- All SQL through the ORM or parameterised queries. Never string-format SQL.
- Validate and bound every external input (size, type, range).
- Use `secrets` for tokens; never `random`.
- Passwords: argon2id via `passlib`; never hash with MD5/SHA-1.
- No secrets in code, tests or logs. Read from the environment via `settings.py`.
- New dependencies need human approval and must be in the internal registry.
