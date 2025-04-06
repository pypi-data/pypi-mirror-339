from unittest.mock import MagicMock


def test_set_priority(cli):
    cli.jira = MagicMock()

    class Args:
        issue_key = "AAP-100"
        priority = "High"

    cli.set_priority(Args())

    cli.jira.set_priority.assert_called_once_with("AAP-100", "High")
