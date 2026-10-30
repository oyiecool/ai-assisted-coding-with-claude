import json

import pytest
from check_plan import classify, main


def plan(*changes):
    return {"format_version": "1.2", "resource_changes": [
        {"address": address, "change": {"actions": actions}} for address, actions in changes
    ]}


def write(tmp_path, data):
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(data))
    return str(path)


NEW_BUCKET = ("aws_s3_bucket.invoice_pdfs", ["create"])
NEW_POLICY = ("aws_s3_bucket_public_access_block.invoice_pdfs", ["create"])


@pytest.mark.parametrize("actions, kind", [
    (["create"], "create"), (["update"], "update"), (["delete"], "delete"),
    (["delete", "create"], "replace"), (["create", "delete"], "replace"),
    (["no-op"], "no-op"), (["read"], "read"),
])
def test_classify(actions, kind):
    assert classify(actions) == kind


def test_create_only_plan_passes(tmp_path, capsys):
    assert main([write(tmp_path, plan(NEW_BUCKET, NEW_POLICY))]) == 0
    assert "Plan: 2 create" in capsys.readouterr().out


def test_unexpected_update_fails(tmp_path, capsys):
    data = plan(NEW_BUCKET, ("aws_s3_bucket.reports", ["update"]))
    assert main([write(tmp_path, data)]) == 1
    assert "update   aws_s3_bucket.reports" in capsys.readouterr().out


def test_replace_fails_even_if_update_is_allowed(tmp_path):
    data = plan(("aws_kms_key.billing", ["delete", "create"]))
    assert main([write(tmp_path, data), "--allow-update", "aws_kms_key.billing"]) == 1


def test_delete_fails(tmp_path):
    assert main([write(tmp_path, plan(("aws_s3_bucket.old", ["delete"])))]) == 1


def test_explicitly_allowed_update_passes(tmp_path):
    data = plan(NEW_BUCKET, ("aws_iam_policy.billing_writer", ["update"]))
    assert main([write(tmp_path, data), "--allow-update", "aws_iam_policy.billing_writer"]) == 0


def test_no_changes_passes(tmp_path, capsys):
    assert main([write(tmp_path, plan())]) == 0
    assert "no changes" in capsys.readouterr().out


def test_wrong_input_exits_two(tmp_path):
    assert main([write(tmp_path, {"not": "a plan"})]) == 2
    bad = tmp_path / "bad.json"
    bad.write_text("{")
    assert main([str(bad)]) == 2
