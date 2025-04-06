def test_block_command(cli, capsys):
    called = {}

    def mock_block_issue(issue_key, reason):
        called["issue_key"] = issue_key
        called["reason"] = reason

    cli.jira.block_issue = mock_block_issue

    class Args:
        issue_key = "AAP-456"
        reason = "Blocked by external dependency"

    cli.block(Args())

    captured = capsys.readouterr()
    assert "✅ AAP-456 marked as blocked" in captured.out
    assert called == {
        "issue_key": "AAP-456",
        "reason": "Blocked by external dependency",
    }


def test_block_command_exception(cli, capsys):
    def mock_block_issue(issue_key, reason):
        raise Exception("Simulated failure")

    cli.jira.block_issue = mock_block_issue

    class Args:
        issue_key = "AAP-789"
        reason = "Something went wrong"

    cli.block(Args())

    captured = capsys.readouterr()
    assert "❌ Failed to mark AAP-789 as blocked: Simulated failure" in captured.out
