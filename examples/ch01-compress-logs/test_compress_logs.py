import gzip
import os
import time

import pytest
from compress_logs import main

DAY = 86400


def make(path, age_days, text="line\n"):
    path.write_text(text)
    t = time.time() - age_days * DAY
    os.utime(path, (t, t))
    return path


@pytest.fixture
def logs(tmp_path):
    make(tmp_path / "old.log", 40, "old contents\n")
    make(tmp_path / "new.log", 1)
    make(tmp_path / "already.log.gz", 40)
    make(tmp_path / "notes.txt", 40)
    return tmp_path


def test_compresses_only_old_logs(logs):
    assert main([str(logs)]) == 0
    assert not (logs / "old.log").exists()
    assert gzip.open(logs / "old.log.gz", "rt").read() == "old contents\n"
    assert (logs / "new.log").exists()
    assert (logs / "notes.txt").exists()
    assert not (logs / "already.log.gz.gz").exists()


def test_dry_run_changes_nothing(logs, caplog):
    caplog.set_level("INFO")
    assert main([str(logs), "--dry-run"]) == 0
    assert (logs / "old.log").exists()
    assert not (logs / "old.log.gz").exists()
    assert "would compress" in caplog.text


def test_keeps_mtime(logs):
    before = (logs / "old.log").stat().st_mtime
    main([str(logs)])
    assert abs((logs / "old.log.gz").stat().st_mtime - before) < 1


def test_failure_gives_nonzero_exit(logs):
    make(logs / "old.log.gz", 1)  # target already exists -> that file fails
    assert main([str(logs)]) == 1
    assert (logs / "old.log").exists()


def test_missing_directory(tmp_path):
    assert main([str(tmp_path / "nope")]) == 2


def test_symlinks_are_ignored(tmp_path):
    real = make(tmp_path / "real.txt", 40)
    link = tmp_path / "link.log"
    link.symlink_to(real)
    main([str(tmp_path)])
    assert link.is_symlink()
