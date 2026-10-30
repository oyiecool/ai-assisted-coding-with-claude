#!/usr/bin/env bats
# Tests for the protect-paths PreToolUse hook (Chapter 7, section 7.11).

HOOK="$BATS_TEST_DIRNAME/.claude/hooks/protect-paths.sh"

hook_input() { printf '{"tool_name":"Edit","tool_input":{"file_path":"%s"}}' "$1"; }

@test "allows ordinary source files" {
  run bash -c "$(declare -f hook_input); hook_input src/app/orders.py | '$HOOK'"
  [ "$status" -eq 0 ]
}

@test "blocks migrations with exit code 2 and a reason" {
  run bash -c "$(declare -f hook_input); hook_input db/migrations/0042_add.py | '$HOOK'"
  [ "$status" -eq 2 ]
  [[ "$output" == *"alembic revision"* ]]
}

@test "blocks generated files" {
  run bash -c "$(declare -f hook_input); hook_input api/generated/client.py | '$HOOK'"
  [ "$status" -eq 2 ]
}

@test "blocks lockfiles" {
  run bash -c "$(declare -f hook_input); hook_input uv.lock | '$HOOK'"
  [ "$status" -eq 2 ]
}

@test "blocks .env files" {
  run bash -c "$(declare -f hook_input); hook_input config/.env.production | '$HOOK'"
  [ "$status" -eq 2 ]
}

@test "ignores tool calls without a path" {
  run bash -c "echo '{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"ls\"}}' | '$HOOK'"
  [ "$status" -eq 0 ]
}
