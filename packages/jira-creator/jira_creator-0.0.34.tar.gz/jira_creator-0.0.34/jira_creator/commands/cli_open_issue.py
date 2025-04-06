import os
import subprocess


def cli_open_issue(args):
    try:
        subprocess.Popen(
            ["xdg-open", os.getenv("JIRA_URL") + "/browse/" + args.issue_key]
        )

    except Exception as e:
        print(f"❌ Failed to open issue {args.issue_key}: {e}")
