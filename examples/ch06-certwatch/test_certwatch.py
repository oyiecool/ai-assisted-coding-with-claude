"""Tests for certwatch. No test touches the network: connect is faked."""
import json
import ssl
from datetime import UTC, datetime

import pytest
from certwatch.cli import main
from certwatch.parse import Target, parse_hosts, parse_line
from certwatch.probe import probe

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def cert(not_after: str, cn: str = "example.com") -> dict:
    return {
        "notAfter": not_after,
        "subject": ((("commonName", cn),),),
        "issuer": ((("organizationName", "Example CA"),), (("commonName", "Example CA R1"),)),
    }


# ---- parsing -------------------------------------------------------------

@pytest.mark.parametrize("line, expected", [
    ("example.com", Target("example.com", 443)),
    ("example.com:8443", Target("example.com", 8443)),
    ("  example.com  # prod  ", Target("example.com", 443)),
    ("[2001:db8::1]", Target("2001:db8::1", 443)),
    ("[2001:db8::1]:8443", Target("2001:db8::1", 8443)),
])
def test_parse_valid(line, expected):
    assert parse_line(line) == expected


@pytest.mark.parametrize("line", ["", "   ", "# only a comment"])
def test_parse_skips_blank_and_comments(line):
    assert parse_line(line) is None


@pytest.mark.parametrize("line", [
    "example.com:0", "example.com:70000", "example.com:https", ":443",
    "[2001:db8::1", "2001:db8::1", "[2001:db8::1]x",
])
def test_parse_invalid(line):
    with pytest.raises(ValueError):
        parse_line(line)


def test_parse_hosts_reports_line_number():
    with pytest.raises(ValueError, match="line 3"):
        parse_hosts("a.example\n# ok\nb.example:99999\n")


# ---- probing -------------------------------------------------------------

def test_days_left_in_utc():
    result = probe(Target("example.com"), connect=lambda *a: cert("Oct 11 12:00:00 2026 GMT"), now=NOW)
    assert result.ok
    assert result.days_left == 10
    assert result.subject == "CN=example.com"
    assert result.issuer == "O=Example CA, CN=Example CA R1"


def test_timeout_is_reported_not_raised():
    def boom(*_):
        raise TimeoutError("timed out")

    result = probe(Target("slow.example"), connect=boom, now=NOW)
    assert not result.ok
    assert "TimeoutError" in result.error


def test_tls_error_is_reported():
    def bad(*_):
        raise ssl.SSLCertVerificationError("certificate has expired")

    result = probe(Target("expired.example"), connect=bad, now=NOW)
    assert "SSLCertVerificationError" in result.error


def test_verify_flag_is_passed_through():
    seen = {}

    def spy(host, port, timeout, verify):
        seen.update(host=host, port=port, timeout=timeout, verify=verify)
        return cert("Oct 11 12:00:00 2026 GMT")

    probe(Target("example.com", 8443), timeout=5.0, verify=False, connect=spy, now=NOW)
    assert seen == {"host": "example.com", "port": 8443, "timeout": 5.0, "verify": False}


# ---- CLI: thresholds, exit codes and JSON ---------------------------------

def fake_connect(certs):
    def connect(host, port, timeout, verify):
        value = certs[host]
        if isinstance(value, Exception):
            raise value
        return value
    return connect


@pytest.fixture
def hosts_file(tmp_path):
    path = tmp_path / "hosts.txt"
    path.write_text("ok.example\nsoon.example\n")
    return path


def far(): return cert("Jan  1 00:00:00 2099 GMT")
def near(): return cert(datetime.now(UTC).replace(microsecond=0).strftime("%b %d %H:%M:%S %Y GMT"))


def test_exit_zero_when_all_ok(hosts_file, capsys):
    code = main([str(hosts_file)], connect=fake_connect({"ok.example": far(), "soon.example": far()}))
    assert code == 0
    assert "OK" in capsys.readouterr().out


def test_exit_one_when_expiring(hosts_file, capsys):
    code = main([str(hosts_file), "--days", "21"],
                connect=fake_connect({"ok.example": far(), "soon.example": near()}))
    assert code == 1
    assert "EXPIRING" in capsys.readouterr().out


def test_exit_one_when_a_host_fails(hosts_file):
    code = main([str(hosts_file)],
                connect=fake_connect({"ok.example": far(), "soon.example": OSError("refused")}))
    assert code == 1


def test_json_output(hosts_file, capsys):
    main([str(hosts_file), "--json"], connect=fake_connect({"ok.example": far(), "soon.example": near()}))
    data = json.loads(capsys.readouterr().out)
    assert [d["status"] for d in data] == ["OK", "EXPIRING"]
    assert data[0]["subject"] == "CN=example.com"


def test_negative_days_rejected(hosts_file):
    with pytest.raises(SystemExit) as exc:
        main([str(hosts_file), "--days", "-1"])
    assert exc.value.code == 2


def test_bad_hosts_file_exits_two(tmp_path, capsys):
    path = tmp_path / "hosts.txt"
    path.write_text("bad:port\n")
    assert main([str(path)]) == 2
    assert "line 1" in capsys.readouterr().err
