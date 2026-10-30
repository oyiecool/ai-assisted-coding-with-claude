import sqlite3

import pytest
import secure_patterns as sp


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")
    c.executemany("INSERT INTO users (email) VALUES (?)", [("a@example.com",), ("b@example.com",)])
    return c


INJECTION = "x' OR '1'='1"


def test_injection_works_against_the_vulnerable_query(conn):
    assert len(sp.find_user_vulnerable(conn, INJECTION)) == 2  # every user leaks


def test_parameterised_query_resists_injection(conn):
    assert sp.find_user(conn, INJECTION) == []
    assert sp.find_user(conn, "a@example.com") == [(1, "a@example.com")]


def test_vulnerable_archive_command_contains_injected_shell():
    assert "; rm -rf ~" in sp.archive_command_vulnerable("x; rm -rf ~", "/data")


def test_archive_uses_argument_list_and_no_shell():
    seen = {}

    def fake_run(args, check):
        seen["args"] = args

    sp.make_archive("backup", "/data dir", run=fake_run)
    assert seen["args"] == ["tar", "czf", "backup.tgz", "--", "/data dir"]


@pytest.mark.parametrize("name", ["", "../x", "-rf"])
def test_archive_rejects_bad_names(name):
    with pytest.raises(ValueError):
        sp.make_archive(name, "/data", run=lambda *a, **k: None)


def test_path_traversal_blocked(tmp_path):
    base = tmp_path / "reports"
    base.mkdir()
    (base / "q1.txt").write_text("ok")
    (tmp_path / "secret.txt").write_text("secret")
    assert sp.read_report(base, "q1.txt") == "ok"
    assert sp.read_report_vulnerable(base, "../secret.txt") == "secret"  # the bug
    with pytest.raises(PermissionError):
        sp.read_report(base, "../secret.txt")


def test_tokens_are_long_and_unique():
    tokens = {sp.make_token() for _ in range(100)}
    assert len(tokens) == 100
    assert all(len(t) >= 40 for t in tokens)
