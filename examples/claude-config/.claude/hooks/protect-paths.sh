#!/usr/bin/env bash
# .claude/hooks/protect-paths.sh  (Chapter 7, section 7.11)
# PreToolUse hook: reads the hook's JSON input on stdin and blocks edits to
# protected paths. Exit code 2 blocks the tool call; the message on stderr
# is shown to Claude so it can choose another approach.
#
# Check the input format and exit-code conventions against the current
# Claude Code hooks documentation before relying on this.
set -euo pipefail

path=$(jq -r '.tool_input.file_path // .tool_input.path // empty')
[ -n "$path" ] || exit 0

case "$path" in
  */migrations/*|migrations/*)
    echo "Blocked: $path is a migration. Create one with 'alembic revision' instead." >&2
    exit 2 ;;
  */generated/*|generated/*)
    echo "Blocked: $path is generated. Change the generator, then regenerate." >&2
    exit 2 ;;
  *.lock)
    echo "Blocked: $path is a lockfile. Change dependencies with the package manager." >&2
    exit 2 ;;
  .env|.env.*|*/.env|*/.env.*)
    echo "Blocked: $path may contain secrets." >&2
    exit 2 ;;
esac
exit 0
