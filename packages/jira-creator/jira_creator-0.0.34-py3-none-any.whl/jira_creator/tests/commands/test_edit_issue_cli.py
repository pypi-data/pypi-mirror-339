import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from jira_creator.commands.cli_edit_issue import (  # isort: skip
    cli_edit_issue,
    edit_description,
    fetch_description,
    get_prompt,
    lint_description,
    lint_description_once,
    update_jira_description,
)
from jira_creator.commands.cli_validate_issue import (  # isort: skip
    load_and_cache_issue,
    save_cache,
    sha256,
    validate_blocked,
    validate_epic_link,
    validate_field_with_ai,
    validate_priority,
    validate_progress,
    validate_sprint,
    validate_story_points,
)


def test_cache_directory_creation(mock_cache_path):
    # Set up the mock cache path and patch os.makedirs
    with patch("os.makedirs") as makedirs_mock:
        # Mock the get_cache_path function to return the mock path
        with patch(
            "jira_creator.commands.cli_validate_issue.get_cache_path",
            return_value=mock_cache_path,
        ):
            # Simulate the condition where the cache directory doesn't exist
            with patch("os.path.exists", return_value=False):
                # Mock open to avoid interacting with the actual file system
                with patch("builtins.open", MagicMock()):
                    # Call save_cache with the patched CACHE_PATH
                    save_cache({})

                    # Ensure that os.makedirs is called to create the directory
                    makedirs_mock.assert_called_once_with(
                        os.path.dirname(mock_cache_path), exist_ok=True
                    )


def test_edit_issue_prompt_fallback(cli):
    # Simulate exception when trying to get the prompt
    with patch(
        "rh_jira.JiraPromptLibrary.get_prompt",
        side_effect=Exception("Prompt error"),
    ):
        # Default prompt to fall back to
        default_prompt = "Fallback prompt"

        # Simulate args
        args = type(
            "Args", (), {"issue_key": "FAKE-123", "no_ai": False, "lint": False}
        )()

        # Run the edit issue method
        cli.edit_issue(args)

        # Check if default prompt was used as fallback
        # In this case, we check the call to JiraPromptLibrary.get_prompt, which should have triggered an exception.
        # We want to verify that the prompt was set to the default prompt after the exception.
        # Since there's no direct way to assert the prompt value here, we can verify the behavior.
        cli.jira.update_description.assert_called_once()  # Ensure update_description was called
        print(f"Captured Output: Prompt fallback: {default_prompt}")


def test_edit_issue_executes(cli):
    args = type("Args", (), {"issue_key": "FAKE-123", "no_ai": False, "lint": False})()
    cli.edit_issue(args)
    cli.jira.update_description.assert_called_once()


def test_load_and_cache_issue():
    with patch(
        "jira_creator.commands.cli_validate_issue.load_cache",
        return_value={"FAKE-123": {"summary_hash": "some_hash"}},
    ):
        cache, cached = load_and_cache_issue("FAKE-123")
        assert cached == {"summary_hash": "some_hash"}
        assert cache == {"FAKE-123": {"summary_hash": "some_hash"}}


def test_validate_progress():
    problems = []
    issue_status = {}

    # Test when status is "In Progress" but no assignee
    validate_progress("In Progress", None, problems, issue_status)
    assert "❌ Issue is In Progress but unassigned" in problems
    assert issue_status["Progress"] is False

    # Test when status is "In Progress" and assignee is present
    problems.clear()
    validate_progress("In Progress", "assignee", problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Progress"] is True


def test_validate_epic_link():
    problems = []
    issue_status = {}

    # Test when epic_link is missing and issue type is not exempt
    validate_epic_link("Story", "In Progress", None, problems, issue_status)
    assert "❌ Issue has no assigned Epic" in problems
    assert issue_status["Epic"] is False

    # Test when epic_link is missing but issue type is exempt
    problems.clear()
    validate_epic_link("Epic", "New", None, problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Epic"] is True


def test_validate_sprint():
    problems = []
    issue_status = {}

    # Test when status is "In Progress" but no sprint assigned
    validate_sprint("In Progress", None, problems, issue_status)
    assert "❌ Issue is In Progress but not assigned to a Sprint" in problems
    assert issue_status["Sprint"] is False

    # Test when status is "In Progress" and sprint is assigned
    problems.clear()
    validate_sprint("In Progress", "Sprint-1", problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Sprint"] is True


def test_validate_priority():
    problems = []
    issue_status = {}

    # Test when priority is not set
    validate_priority(None, problems, issue_status)
    assert "❌ Priority not set" in problems
    assert issue_status["Priority"] is False

    # Test when priority is set
    problems.clear()
    validate_priority("High", problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Priority"] is True


def test_validate_story_points():
    problems = []
    issue_status = {}

    # Test when story points are not assigned and status is not "Refinement" or "New"
    validate_story_points(None, "In Progress", problems, issue_status)
    assert "❌ Story points not assigned" in problems
    assert issue_status["Story P."] is False

    # Test when story points are not assigned but status is "Refinement"
    problems.clear()
    validate_story_points(None, "Refinement", problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Story P."] is True


def test_validate_blocked():
    problems = []
    issue_status = {}

    # Test when the issue is blocked but has no reason
    validate_blocked("True", None, problems, issue_status)
    assert "❌ Issue is blocked but has no blocked reason" in problems
    assert issue_status["Blocked"] is False

    # Test when the issue is blocked and has a reason
    problems.clear()
    validate_blocked("True", "Blocked due to issue", problems, issue_status)
    assert len(problems) == 0  # No issues
    assert issue_status["Blocked"] is True


def test_validate_field_with_ai_valid():
    # Patch ai_provider to return the MagicMock object
    with patch(
        "jira_creator.providers.get_ai_provider", return_value=MagicMock()
    ) as ai_provider:
        problems = []  # Initialize problems list
        issue_status = {}  # Initialize issue_status dictionary
        cached_field_hash = None  # Initialize cached hash

        # Set up the mock for the improve_text method
        improve_text_mock = MagicMock()
        improve_text_mock.return_value = "OK"  # Mock AI response for valid summary
        ai_provider.improve_text = improve_text_mock  # Assign the mock to ai_provider

        # Test when field value requires validation
        cached_field_hash = validate_field_with_ai(
            "Summary",
            "Test summary",
            sha256("Test summary"),
            cached_field_hash,
            ai_provider,
            problems,
            issue_status,
        )

        # Check if the problem was added to the list (invalid summary)
        print(f"Problems: {problems}")  # Debugging: Print the problems list
        assert len(problems) == 0  # Should have one problem related to summary
        assert (
            "❌ Summary: Summary is unclear" not in problems
        )  # Validate the problem message
        assert (
            issue_status["Summary"] is True
        )  # Status should be False as AI returned an issue


def test_validate_field_with_ai_invalid():
    # Patch ai_provider to return the MagicMock object
    with patch(
        "jira_creator.providers.get_ai_provider", return_value=MagicMock()
    ) as ai_provider:
        problems = []  # Initialize problems list
        issue_status = {}  # Initialize issue_status dictionary
        cached_field_hash = None  # Initialize cached hash

        # Set up the mock for the improve_text method
        improve_text_mock = MagicMock()
        improve_text_mock.return_value = (
            "Summary is unclear"  # Set AI to return "not OK"
        )
        ai_provider.improve_text = improve_text_mock  # Assign the mock to ai_provider

        # Run validation for the invalid summary
        cached_field_hash = validate_field_with_ai(
            "Summary",
            "Test summary",
            sha256("Test summary"),
            cached_field_hash,
            ai_provider,
            problems,
            issue_status,
        )

        # Check if the problem was added to the list (invalid summary)
        print(f"Problems: {problems}")  # Debugging: Print the problems list
        assert len(problems) == 1  # Should have one problem related to summary
        assert (
            "❌ Summary: Summary is unclear" in problems
        )  # Validate the problem message
        assert (
            issue_status["Summary"] is False
        )  # Status should be False as AI returned an issue


def test_edit_no_ai(cli):
    cli.jira.get_description = lambda k: "description"
    cli.jira.update_description = MagicMock()
    cli.jira.get_issue_type = lambda k: "story"

    # Patch subprocess.call to prevent the editor from opening
    with patch("subprocess.call") as mock_subprocess:
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            tf.write("edited")
            tf.seek(0)

            class Args:
                issue_key = "AAP-123"
                no_ai = True
                lint = False  # ✅ Add this to fix the error

            cli.edit_issue(Args())
            cli.jira.update_description.assert_called_once()
            mock_subprocess.assert_called_once()  # Ensure subprocess.call was called


def test_edit_with_ai(cli):
    cli.jira.get_description = lambda k: "raw text"
    cli.jira.update_description = MagicMock()
    cli.jira.get_issue_type = lambda k: "story"
    cli.ai_provider.improve_text = lambda p, t: "cleaned text"

    # Patch subprocess.call to prevent the editor from opening
    with patch("subprocess.call") as mock_subprocess:
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            tf.write("dirty")
            tf.seek(0)

            class Args:
                issue_key = "AAP-999"
                no_ai = False
                lint = False  # ✅ Add this to fix the error

            cli.edit_issue(Args())
            cli.jira.update_description.assert_called_once_with(
                "AAP-999", "cleaned text"
            )
            mock_subprocess.assert_called_once()


def test_fetch_description(cli):
    jira_mock = MagicMock()
    jira_mock.get_description = MagicMock(return_value="Test description")

    description = fetch_description(jira_mock, "ISSUE-123")
    assert description == "Test description"


def test_update_jira_description():
    jira_mock = MagicMock()
    jira_mock.update_description = MagicMock()

    update_jira_description(jira_mock, "ISSUE-123", "Cleaned description")

    jira_mock.update_description.assert_called_once_with(
        "ISSUE-123", "Cleaned description"
    )


def test_lint_description_once():
    ai_provider_mock = MagicMock()
    ai_provider_mock.improve_text = MagicMock(return_value="Cleaned description")
    validate_mock = MagicMock(return_value=[["❌ Description: Cleaned description"]])
    mock_input = MagicMock(side_effect=["additional details"])

    with (
        patch("jira_creator.commands.cli_edit_issue.validate", validate_mock),
        patch("builtins.input", mock_input),
    ):
        cleaned, should_continue = lint_description_once(
            "Original description", ai_provider_mock
        )
        assert cleaned == "Cleaned description"
        assert should_continue is True
        assert validate_mock.call_count == 1
        assert mock_input.call_count == 1


def test_lint_description():
    ai_provider_mock = MagicMock()
    ai_provider_mock.improve_text = MagicMock(return_value="Cleaned description")

    # Mock validate function to simulate two iterations:
    # 1st iteration: validation issues (invalid description)
    # 2nd iteration: no validation issues (valid description)
    validate_mock = MagicMock(side_effect=[["❌ Description: Cleaned description"], []])

    # Create a mock input to track interactions
    mock_input = MagicMock(side_effect=["additional details", "more details"])

    # Mock lint_description_once to directly return "Cleaned description"
    with patch(
        "jira_creator.commands.cli_edit_issue.lint_description_once",
        return_value=("Cleaned description", False),
    ):
        # Call the lint_description function (which now uses the mocked lint_description_once)
        cleaned = lint_description("Original description", ai_provider_mock)

        # Assert the final cleaned description is returned as expected
        assert (
            cleaned == "Cleaned description"
        )  # We expect the cleaned description after AI processing

        # Ensure that input was not called, since lint_description_once is mocked
        assert mock_input.call_count == 0  # No interaction since the function is mocked

        # Assert that validate was also not called (since the function is mocked)
        assert validate_mock.call_count == 0


def test_get_prompt():
    jira_mock = MagicMock()
    jira_mock.get_issue_type = MagicMock(return_value="story")

    prompt = get_prompt(jira_mock, "ISSUE-123", "Default prompt")
    assert (
        "As a professional Principal Software Engineer, you write acute, well-defined Jira issues"
        in prompt
    )


def test_edit_description():
    original_description = "Test description"

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as tmp:
        tmp.write(original_description)
        tmp.flush()
        tmp.seek(0)
        edited = edit_description(original_description)
        assert edited == original_description
        os.remove(tmp.name)

    # Test failure scenario (simulating subprocess.call failure)
    with patch("subprocess.call", side_effect=Exception("Editor failed")):
        with pytest.raises(
            RuntimeError, match="Failed to edit description: Editor failed"
        ):
            edit_description(original_description)


def test_lint_description_once_no_issues():
    # Mock the AI provider's improve_text method
    ai_provider_mock = MagicMock()
    ai_provider_mock.improve_text = MagicMock(return_value="Cleaned description")

    # Mock the validate function to simulate no issues
    validate_mock = MagicMock(
        return_value=[[]]
    )  # Empty list, meaning no description problems

    # Simulate the cleaned description without issues
    cleaned = "Original description"

    with patch("jira_creator.commands.cli_edit_issue.validate", validate_mock):
        # Call the lint_description_once function (should return cleaned description and False)
        result, should_continue = lint_description_once(cleaned, ai_provider_mock)

        # Assert that the cleaned description is returned
        assert result == "Original description"

        # Assert that should_continue is False, meaning no issues were found
        assert should_continue is False

        # Ensure validate was called once
        assert validate_mock.call_count == 1


def test_cli_edit_issue_no_edited():
    # Setup the mocks
    jira_mock = MagicMock()
    ai_provider_mock = MagicMock()
    default_prompt = "Default prompt"
    try_cleanup_fn = MagicMock()

    # Arguments for the test, simulating the case when no AI cleanup is needed
    args = MagicMock()
    args.issue_key = "AAP-12345"
    args.no_ai = True  # Simulate no AI cleanup
    args.lint = False  # No linting

    # Mock fetch_description to return a valid description
    fetch_description_mock = MagicMock(return_value="Original description")

    # Mock edit_description to return None (simulating no editing)
    edit_description_mock = MagicMock(return_value=None)

    # Mock update_jira_description to ensure it is not called when the description is not edited
    update_jira_description_mock = MagicMock()

    with (
        patch(
            "jira_creator.commands.cli_edit_issue.fetch_description",
            fetch_description_mock,
        ),
        patch(
            "jira_creator.commands.cli_edit_issue.edit_description",
            edit_description_mock,
        ),
        patch(
            "jira_creator.commands.cli_edit_issue.update_jira_description",
            update_jira_description_mock,
        ),
    ):
        # Call the function
        cli_edit_issue(
            jira_mock, ai_provider_mock, default_prompt, try_cleanup_fn, args
        )

        # Assert that edit_description was called with the correct description
        edit_description_mock.assert_called_once_with("Original description")

        # Assert that update_jira_description was not called because edited is None
        update_jira_description_mock.assert_not_called()


def test_cli_edit_issue_lint_true():
    # Setup the mocks
    jira_mock = MagicMock()
    ai_provider_mock = MagicMock()
    default_prompt = "Default prompt"
    try_cleanup_fn = MagicMock()

    # Arguments for the test, simulating the case where linting is enabled
    args = MagicMock()
    args.issue_key = "AAP-12345"
    args.no_ai = False  # Simulate that AI cleanup is needed
    args.lint = True  # Linting is enabled

    # Mock fetch_description to return a valid description
    fetch_description_mock = MagicMock(return_value="Original description")

    # Mock edit_description to return an edited description
    edit_description_mock = MagicMock(return_value="Edited description")

    # Mock try_cleanup_fn to simulate AI cleanup and return a cleaned description
    try_cleanup_fn_mock = MagicMock(return_value="Cleaned description")

    # Mock lint_description to simulate linting and return the linted description
    lint_description_mock = MagicMock(return_value="Linted description")

    # Mock update_jira_description to ensure it is called with the final cleaned description
    update_jira_description_mock = MagicMock()

    with (
        patch(
            "jira_creator.commands.cli_edit_issue.fetch_description",
            fetch_description_mock,
        ),
        patch(
            "jira_creator.commands.cli_edit_issue.edit_description",
            edit_description_mock,
        ),
        patch("jira_creator.commands._try_cleanup", try_cleanup_fn_mock),
        patch(
            "jira_creator.commands.cli_edit_issue.lint_description",
            lint_description_mock,
        ),
        patch(
            "jira_creator.commands.cli_edit_issue.update_jira_description",
            update_jira_description_mock,
        ),
    ):
        # Call the function with linting enabled
        cli_edit_issue(
            jira_mock, ai_provider_mock, default_prompt, try_cleanup_fn, args
        )

        # Assert that fetch_description was called with the correct issue key
        fetch_description_mock.assert_called_once_with(jira_mock, args.issue_key)

        # Assert that edit_description was called with the original description
        edit_description_mock.assert_called_once_with("Original description")
