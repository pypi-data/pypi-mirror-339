import os
import subprocess
import tempfile

from commands.cli_validate_issue import cli_validate_issue as validate
from rest.jira_prompts import JiraIssueType, JiraPromptLibrary


def fetch_description(jira, issue_key):
    try:
        print("Fetching description...")
        return jira.get_description(issue_key)
    except Exception as e:
        print(f"❌ Failed to fetch description: {e}")
        return None


def edit_description(original_description):
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as tmp:
            tmp.write(original_description or "")
            tmp.flush()
            subprocess.call(
                [os.environ.get("EDITOR", "vim"), tmp.name]
            )  # This can raise an exception
            tmp.seek(0)
            return tmp.read()
    except Exception as e:
        error_message = f"❌ Failed to edit description: {e}"
        print(error_message)  # This would be captured in the logs
        raise RuntimeError(error_message)


def get_prompt(jira, issue_key, default_prompt):
    try:
        print("Getting Jira prompt...")
        return JiraPromptLibrary.get_prompt(
            JiraIssueType(jira.get_issue_type(issue_key).lower())
        )
    except Exception:
        print("❌ Failed to get Jira prompt, using default prompt.")
        return default_prompt


def lint_description_once(cleaned, ai_provider):
    """
    This function encapsulates the linting logic for one iteration of the loop.
    It validates the description and interacts with the user to improve the description.
    """
    fields = {"key": "AAP-12345", "description": cleaned}
    problems = validate(fields, ai_provider)[0]
    print(f"Validation issues: {problems}")

    description_problems = [p for p in problems if p.startswith("❌ Description:")]
    print(f"Description problems: {description_problems}")

    if not description_problems:
        return cleaned, False  # No issues found, no need to continue

    print("\n⚠️ Description Lint Issues:")
    for p in description_problems:
        print(f" - {p}")

    print("\n📝 Please provide more information given the problems stated above:")
    user_answers = input("> ").strip()
    print(f"User entered: {user_answers}")

    prompt = (
        "Incorporate these additional details into the below Jira description.\n"
        f"Details to incorporate: {user_answers}\n"
        "Original description:\n"
        f"{cleaned}"
    )

    # Generate the updated description
    cleaned = ai_provider.improve_text(prompt, cleaned)
    print(f"Updated cleaned description: {cleaned}")  # Debugging print

    return cleaned, True  # There are still issues, continue the loop


def lint_description(cleaned, ai_provider):
    print("Starting linting...")
    while True:
        print(f"Current cleaned description: {cleaned}")  # Debugging print

        # Call the refactored function
        cleaned, should_continue = lint_description_once(cleaned, ai_provider)

        if should_continue is False:
            print("No issues found, breaking out of loop.")
            break

    print("\n🤖 Final description:\n")
    print(cleaned)
    return cleaned


def update_jira_description(jira, issue_key, cleaned):
    try:
        print("Updating Jira description...")
        jira.update_description(issue_key, cleaned)
        print(f"✅ Updated {issue_key}")
    except Exception as e:
        print(f"❌ Update failed: {e}")


def cli_edit_issue(jira, ai_provider, default_prompt, try_cleanup_fn, args):
    original_description = fetch_description(jira, args.issue_key)
    if not original_description:
        return

    edited = edit_description(original_description)
    if not edited:
        return

    prompt = get_prompt(jira, args.issue_key, default_prompt)

    cleaned = edited if args.no_ai else try_cleanup_fn(ai_provider, prompt, edited)
    if args.lint:
        cleaned = lint_description(cleaned, ai_provider)

    update_jira_description(jira, args.issue_key, cleaned)
