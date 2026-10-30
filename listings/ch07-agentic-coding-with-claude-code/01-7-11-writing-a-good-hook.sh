#!/usr/bin/env bash
# .claude/hooks/protect-paths.sh
# Reads the hook's JSON input on stdin; blocks edits to protected paths.
set -euo pipefail
path=$(jq -r '.tool_input.file_path // empty')
case "$path" in
  */migrations/*|*/generated/*|*.lock)
    echo "Blocked: $path is protected. Use the documented tool instead." >&2
    exit 2 ;;
esac
exit 0
