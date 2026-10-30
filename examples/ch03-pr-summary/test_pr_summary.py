"""Tests for pr_summary. A fake client stands in for the API; no network."""
from types import SimpleNamespace

import pr_summary


class FakeClient:
    def __init__(self):
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(text="Purpose: tidy up")])


def test_empty_diff_stops_early():
    assert pr_summary.check_diff("   \n") == "No changes."


def test_large_diff_is_refused_not_truncated():
    assert "split the PR" in pr_summary.check_diff("x" * (pr_summary.MAX_DIFF_CHARS + 1))


def test_normal_diff_is_accepted():
    assert pr_summary.check_diff("+print('hi')\n") is None


def test_diff_is_wrapped_in_delimiters():
    content = pr_summary.build_messages("+a = 1")[0]["content"]
    assert content.startswith("<diff>\n") and content.endswith("\n</diff>")


def test_summarise_sends_system_prompt_and_returns_text():
    client = FakeClient()
    assert pr_summary.summarise("+a = 1", client=client) == "Purpose: tidy up"
    call = client.calls[0]
    assert "Never invent behaviour" in call["system"]
    assert call["max_tokens"] == 1500


def test_main_exit_codes(monkeypatch, capsys):
    monkeypatch.setattr(pr_summary, "get_diff", lambda base: "")
    assert pr_summary.main([]) == 0
    monkeypatch.setattr(pr_summary, "get_diff", lambda base: "x" * 300_000)
    assert pr_summary.main([]) == 1
    assert "split the PR" in capsys.readouterr().out
