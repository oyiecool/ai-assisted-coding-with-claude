#!/usr/bin/env bats
# tests/rotate_logs.bats

setup() {
  TMP=$(mktemp -d)
  touch -d '40 days ago' "$TMP/old.log"
  touch "$TMP/new.log"
  touch -d '40 days ago' "$TMP/already.log.gz"
}
teardown() { rm -rf "$TMP"; }

@test "compresses only logs older than 30 days" {
  run ./rotate_logs.sh "$TMP"
  [ "$status" -eq 0 ]
  [ -f "$TMP/old.log.gz" ]
  [ -f "$TMP/new.log" ]
}

@test "dry run changes nothing" {
  run ./rotate_logs.sh --dry-run "$TMP"
  [ "$status" -eq 0 ]
  [ -f "$TMP/old.log" ]
  [ ! -f "$TMP/old.log.gz" ]
}

@test "fails clearly on a missing directory" {
  run ./rotate_logs.sh /no/such/dir
  [ "$status" -ne 0 ]
}
