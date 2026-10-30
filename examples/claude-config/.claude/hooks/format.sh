#!/usr/bin/env bash
# .claude/hooks/format.sh  (Chapter 4, section 4.5)
# PostToolUse hook: format only the file that was just edited, so the hook
# stays fast. Never fails the session: formatting problems are reported,
# not fatal.
set -uo pipefail

path=$(jq -r '.tool_input.file_path // empty')
[ -n "$path" ] && [ -f "$path" ] || exit 0

case "$path" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format --quiet "$path" || echo "format.sh: ruff could not format $path" >&2
    fi ;;
  *.sh)
    if command -v shfmt >/dev/null 2>&1; then
      shfmt -w -i 2 "$path" || echo "format.sh: shfmt could not format $path" >&2
    fi ;;
esac
exit 0
