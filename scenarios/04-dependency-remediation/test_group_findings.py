import json
from pathlib import Path

import pytest
from group_findings import main, minimal_fix, plan_upgrades

SAMPLES = Path(__file__).parent / "sample-audits"


def audits():
    return {p.stem: json.loads(p.read_text())["dependencies"] for p in SAMPLES.glob("*.json")}


def by_package(upgrades):
    return {u.package: u for u in upgrades}


def test_minimal_fix_prefers_patch_release_over_new_major():
    # urllib3 1.26.17 is fixed in both 1.26.18 and 2.0.7: take the 1.x patch.
    assert str(minimal_fix("1.26.17", ["1.26.18", "2.0.7"])) == "1.26.18"


def test_minimal_fix_ignores_versions_not_above_installed():
    assert minimal_fix("2.0.0", ["1.9.9", "2.0.0"]) is None


def test_target_fixes_all_findings_for_the_package():
    up = by_package(plan_upgrades(audits()))
    assert up["jinja2"].target == "3.1.4"     # 3.1.3 would leave one finding open
    assert up["urllib3"].target == "1.26.19"  # not 2.x
    assert up["requests"].target == "2.32.0"


def test_package_names_are_grouped_case_insensitively_across_services():
    up = by_package(plan_upgrades(audits()))
    assert up["jinja2"].services == ["billing", "portal"]
    assert up["requests"].services == ["billing", "search"]


def test_findings_are_labelled_by_cve():
    up = by_package(plan_upgrades(audits()))
    assert up["jinja2"].findings == ["CVE-2024-22195", "CVE-2024-34064"]


def test_unfixed_findings_are_listed_first_and_flagged():
    upgrades = plan_upgrades(audits())
    assert upgrades[0].package == "example-legacy-xml"
    assert upgrades[0].target is None
    assert upgrades[0].unfixed == ["PYSEC-0000-EXAMPLE"]


def test_cli_exit_code_signals_unfixed_findings(capsys):
    files = [str(p) for p in sorted(SAMPLES.glob("*.json"))]
    assert main(files) == 1
    out = capsys.readouterr().out
    assert "9 findings -> 4 package upgrades" in out
    assert "UPGRADE  jinja2 3.1.2 -> 3.1.4  [billing, portal]" in out


def test_cli_exit_zero_when_everything_has_a_fix(capsys):
    assert main([str(SAMPLES / "billing.json")]) == 0


def test_old_list_layout_is_supported(tmp_path):
    path = tmp_path / "svc.json"
    path.write_text(json.dumps([{"name": "x", "version": "1.0", "vulns": [
        {"id": "GHSA-x", "fix_versions": ["1.0.1"]}]}]))
    assert main([str(path)]) == 0


@pytest.mark.parametrize("content", ["not json", "{}"])
def test_bad_input_exits_two(tmp_path, content):
    path = tmp_path / "bad.json"
    path.write_text(content)
    assert main([str(path)]) == 2
