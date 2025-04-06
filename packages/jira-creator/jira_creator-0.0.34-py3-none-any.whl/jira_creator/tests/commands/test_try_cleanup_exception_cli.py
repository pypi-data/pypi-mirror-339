from unittest.mock import MagicMock


def test_try_cleanup_error(cli):
    # Mock the AI provider's improve_text method to simulate an exception
    cli.ai_provider = MagicMock()
    cli.ai_provider.improve_text.side_effect = Exception("fail")

    # Call _try_cleanup and assert the result
    result = cli._try_cleanup("prompt", "text")
    assert result == "text"
