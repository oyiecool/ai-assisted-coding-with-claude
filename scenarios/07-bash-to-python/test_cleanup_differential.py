"""Differential test: the Bash original and the Python port must agree.

Builds a temporary tree with old and new files, nested directories, names
with spaces, a symlink and files near the whole-day boundary. Then runs BOTH
scripts with --dry-run and compares the sorted lists of files each would
delete. Written before the port, as the scenario's brief requires.
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import cleanup_tmp
import pytest

HERE = Path(__file__).parent
DAY = 86400

pytestmark = pytest.mark.skipif(shutil.which("bash") is None or shutil.which("find") is None,
                                reason="needs bash and GNU find")


def touch(path: Path, age_days: float):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x")
    t = time.time() - age_days * DAY
    os.utime(path, (t, t))


@pytest.fixture
def tree(tmp_path):
    root = tmp_path / "tmpdir"
    touch(root / "old.txt", 30)
    touch(root / "new.txt", 1)
    touch(root / "nested" / "deeper" / "old report.csv", 12)
    touch(root / "nested" / "fresh.csv", 2)
    touch(root / "boundary-7.5-days.txt", 7.5)    # 7 whole days: NOT older than +7
    touch(root / "boundary-8.2-days.txt", 8.2)    # 8 whole days: matched
    outside = tmp_path / "outside-old.txt"
    touch(outside, 40)
    (root / "link-to-outside.txt").symlink_to(outside)
    (root / "linked-dir").symlink_to(tmp_path)
    return root


def run_bash(*args):
    out = subprocess.run(["bash", str(HERE / "cleanup_tmp.sh"), *args],
                         capture_output=True, text=True, check=True, env={**os.environ, "LC_ALL": "C"})
    return out.stdout.splitlines()


def run_python(*args):
    out = subprocess.run([sys.executable, str(HERE / "cleanup_tmp.py"), *args],
                         capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


@pytest.mark.parametrize("days", ["0", "7", "10", "100"])
def test_same_files_selected(tree, days):
    assert run_python("--dry-run", "--days", days, str(tree)) == \
        run_bash("--dry-run", "--days", days, str(tree))


def test_boundary_semantics_match_find(tree):
    selected = {Path(p).name for p in run_python("--dry-run", "--days", "7", str(tree))}
    assert "boundary-8.2-days.txt" in selected
    assert "boundary-7.5-days.txt" not in selected


def test_symlinks_never_followed_or_deleted(tree, tmp_path):
    cleanup_tmp.main(["--days", "7", str(tree)])
    assert (tree / "link-to-outside.txt").is_symlink()
    assert (tmp_path / "outside-old.txt").exists()


def test_real_run_deletes_only_matches(tree):
    cleanup_tmp.main(["--days", "7", str(tree)])
    assert not (tree / "old.txt").exists()
    assert (tree / "new.txt").exists()
    assert (tree / "boundary-7.5-days.txt").exists()


def test_missing_directory_is_a_clear_error(tmp_path, capsys):
    assert cleanup_tmp.main([str(tmp_path / "nope")]) == 2
    assert "not a directory" in capsys.readouterr().err


def test_negative_days_rejected(tmp_path):
    assert cleanup_tmp.main(["--days", "-1", str(tmp_path)]) == 2
