#!/usr/bin/env bats
# Behaviour tests for rotate_logs.sh (Chapter 9, section 9.10).
# Every test runs in a temporary directory; nothing touches real paths.

SCRIPT="$BATS_TEST_DIRNAME/rotate_logs.sh"

setup() {
  TMP=$(mktemp -d)
  touch -d '40 days ago' "$TMP/old.log"
  touch "$TMP/new.log"
  touch -d '40 days ago' "$TMP/already.log.gz"
}

teardown() { rm -rf "$TMP"; }

@test "compresses only logs older than 30 days" {
  run "$SCRIPT" "$TMP"
  [ "$status" -eq 0 ]
  [ -f "$TMP/old.log.gz" ]
  [ ! -f "$TMP/old.log" ]
  [ -f "$TMP/new.log" ]
  [ ! -f "$TMP/already.log.gz.gz" ]
}

@test "dry run changes nothing" {
  run "$SCRIPT" --dry-run "$TMP"
  [ "$status" -eq 0 ]
  [ -f "$TMP/old.log" ]
  [ ! -f "$TMP/old.log.gz" ]
  [[ "$output" == *"would compress"* ]]
}

@test "fails clearly on a missing directory" {
  run "$SCRIPT" /no/such/dir
  [ "$status" -ne 0 ]
  [[ "$output" == *"not a directory"* ]]
}

@test "handles names with spaces" {
  touch -d '40 days ago' "$TMP/web server.log"
  run "$SCRIPT" "$TMP"
  [ "$status" -eq 0 ]
  [ -f "$TMP/web server.log.gz" ]
}

@test "does not follow symlinks" {
  target=$(mktemp)
  touch -d '40 days ago' "$target"
  ln -s "$target" "$TMP/link.log"
  run "$SCRIPT" "$TMP"
  [ -L "$TMP/link.log" ]
  [ -f "$target" ]
  rm -f "$target"
}

@test "rejects a non-numeric --days" {
  run "$SCRIPT" --days ten "$TMP"
  [ "$status" -eq 2 ]
}
