from pathlib import Path

import pytest
from ai_metrics import bucket, compare, load, main, summarise, yes

SAMPLE = Path(__file__).parent / "sample-prs.csv"


def write(tmp_path, lines):
    path = tmp_path / "prs.csv"
    header = "pr,merged_at,ai_assisted,lead_time_hours,lines_changed,caused_incident\n"
    path.write_text(header + "\n".join(lines) + "\n")
    return str(path)


@pytest.mark.parametrize("lines, name", [(0, "S"), (99, "S"), (100, "M"), (499, "M"), (500, "L")])
def test_bucket_edges(lines, name):
    assert bucket(lines) == name


@pytest.mark.parametrize("value, expected", [("yes", True), ("No", False), ("1", True), ("false", False)])
def test_yes(value, expected):
    assert yes(value) is expected


def test_yes_rejects_unknown_values():
    with pytest.raises(ValueError):
        yes("maybe")


def test_summary_figures(tmp_path):
    rows = load(write(tmp_path, [
        "1,2026-10-01,yes,4,50,no",
        "2,2026-10-02,yes,8,60,yes",
        "3,2026-10-03,yes,6,70,no",
    ]))
    group = summarise(rows)
    assert group.count == 3
    assert group.median_lead_time == 6
    assert group.failure_rate == pytest.approx(1 / 3)
    assert group.small


def test_comparison_is_made_within_size_buckets(tmp_path):
    rows = load(write(tmp_path, [
        "1,2026-10-01,yes,30,800,no",    # large AI PR
        "2,2026-10-02,no,5,20,no",       # small other PR
    ]))
    table = compare(rows)
    assert table["L"]["ai"].count == 1 and table["L"]["other"].count == 0
    assert table["S"]["other"].count == 1 and table["S"]["ai"].count == 0


def test_sample_shows_why_the_all_row_misleads():
    """In the sample, AI-assisted PRs are faster in every size bucket with
    enough data, yet slower overall, because they are larger on average."""
    table = compare(load(SAMPLE))
    for size in ("S", "M"):
        assert table[size]["ai"].median_lead_time < table[size]["other"].median_lead_time
    assert table["all"]["ai"].median_lead_time > table["all"]["other"].median_lead_time


def test_cli(capsys):
    assert main([str(SAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "AI-assisted" in out and "treat as noise" in out


def test_cli_bad_input(tmp_path):
    assert main([write(tmp_path, ["1,2026-10-01,perhaps,4,50,no"])]) == 2
    assert main([]) == 2
