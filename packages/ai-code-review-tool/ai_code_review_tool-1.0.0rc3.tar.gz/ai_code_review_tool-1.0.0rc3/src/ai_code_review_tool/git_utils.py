import subprocess
from typing import List


def get_changed_files() -> List[str]:
    """
    Returns a list of staged file paths (relative to repo root).
    """
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            text=True
        )
        return output.strip().splitlines()
    except subprocess.CalledProcessError:
        return []


def generate_commit_message(changed_files: List[str]) -> str:
    """
    Generates a commit message summary based on a list of changed files.
    """
    if not changed_files:
        return "🔄 No staged changes to commit."

    additions = [f for f in changed_files if f.startswith("src/") and f.endswith(".py")]
    docs = [f for f in changed_files if f.startswith("docs/")]
    tests = [f for f in changed_files if f.startswith("tests/")]

    msg = "🔖 Auto-release commit:\n"
    if additions:
        msg += f"➕ {len(additions)} source file(s) updated\n"
    if tests:
        msg += f"🧪 {len(tests)} test file(s) updated\n"
    if docs:
        msg += f"📝 {len(docs)} doc file(s) updated\n"
    others = set(changed_files) - set(additions + docs + tests)
    if others:
        msg += f"📦 {len(others)} misc file(s) updated\n"

    return msg.strip()


def commit_and_push(commit_msg: str):
    """
    Commits staged changes with the provided message and pushes to origin.
    """
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push"], check=True)
