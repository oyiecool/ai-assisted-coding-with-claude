"""Insecure patterns and their fixes (Chapter 11, section 11.7).

Each pair shows a pattern reviewers often find in generated code, and the
fix. The vulnerable versions are here for teaching and for the tests that
prove the fixes work. Never copy them into real code.
"""
from __future__ import annotations

import secrets
import sqlite3
import subprocess
from pathlib import Path

# --- SQL built from strings ------------------------------------------------


def find_user_vulnerable(conn: sqlite3.Connection, email: str) -> list[tuple]:
    # VULNERABLE: user input is formatted into the SQL text.
    return conn.execute(f"SELECT id, email FROM users WHERE email = '{email}'").fetchall()


def find_user(conn: sqlite3.Connection, email: str) -> list[tuple]:
    # Fixed: parameterised query; the driver handles quoting.
    return conn.execute("SELECT id, email FROM users WHERE email = ?", (email,)).fetchall()


# --- Shell commands built from input ---------------------------------------


def archive_command_vulnerable(name: str, path: str) -> str:
    # VULNERABLE when run with shell=True: name could be "x; rm -rf ~".
    return f"tar czf {name}.tgz {path}"


def make_archive(name: str, path: str, run=subprocess.run) -> list[str]:
    # Fixed: an argument list and no shell, so input is never parsed as shell.
    if not name or "/" in name or name.startswith("-"):
        raise ValueError("invalid archive name")
    args = ["tar", "czf", f"{name}.tgz", "--", path]
    run(args, check=True)
    return args


# --- Path traversal ---------------------------------------------------------


def read_report_vulnerable(base: Path, filename: str) -> str:
    # VULNERABLE: "../../etc/passwd" escapes base.
    return (base / filename).read_text()


def read_report(base: Path, filename: str) -> str:
    # Fixed: resolve, then confirm the path stays inside base.
    target = (base / filename).resolve()
    if not target.is_relative_to(base.resolve()):
        raise PermissionError("invalid path")
    return target.read_text()


# --- Weak randomness for secrets --------------------------------------------


def make_token() -> str:
    # Fixed: the secrets module, never random.choice, for anything secret.
    return secrets.token_urlsafe(32)
