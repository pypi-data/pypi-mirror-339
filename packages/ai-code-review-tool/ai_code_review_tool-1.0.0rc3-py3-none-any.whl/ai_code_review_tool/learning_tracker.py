# src/ai_code_review_tool/learning_tracker.py

import json
import os
from datetime import datetime
from typing import Dict
import glob

LEARNING_FILE = "docs/learning_progress.json"
BASELINE_FILE = "docs/.baseline_snapshot.json"

def initialize_learning_baseline(snapshot: dict):
    """
    Save the baseline snapshot from the first known working state of the codebase.
    This file should only be generated once at the start of learning.
    """
    if not os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        print("✅ Learning baseline initialized.")
    else:
        print("ℹ️ Baseline already exists. Skipping initialization.")

def update_learning_progress(changes: Dict[str, list]) -> str:
    """
    Update the learning progress file with details of what was changed or added,
    and return a markdown string summary for docs.
    """
    log = {
        "timestamp": datetime.now().isoformat(),
        "added": changes.get("added", []),
        "removed": changes.get("removed", []),
        "modified": changes.get("modified", [])
    }

    history = []
    if os.path.exists(LEARNING_FILE):
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append(log)

    with open(LEARNING_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print("🧠 Learning progress updated.")

    # Generate summary block for CLI docs
    summary = "## 🧠 Learning Progress & Concepts\n\n"
    summary += "```markdown\n"

    if not os.path.exists("tests/test_troubleshoot_code_errors.py"):
        summary += "- [ ] Learn how to write basic unit tests with `pytest`\n"
    if not os.path.exists("docs/architecture.md"):
        summary += "- [ ] Learn how to diagram project architecture and module relationships\n"
    if not glob.glob("reviews/*.md"):
        summary += "- [ ] Understand how to run an AI-driven review and read structured feedback\n"
    if not glob.glob("patches/*.patch"):
        summary += "- [ ] Learn to read and write patch files for applying suggested changes\n"

    summary += "- [ ] Understand how CLI tools work with Typer\n"
    summary += "- [ ] Learn how to structure a Python project with modules and commands\n"
    summary += "- [ ] Learn how to publish a Python package to PyPI\n"
    summary += "- [ ] Learn how to track changes with Git and structure nightly updates\n"
    summary += "```\n\n"

    return summary

def summarize_learning_progress():
    """
    Provide a text summary of progress made so far.
    """
    if not os.path.exists(LEARNING_FILE):
        return "No learning progress has been recorded yet."

    with open(LEARNING_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    summary = "# 🧠 Learning Tracker Progress Summary\n\n"
    for i, entry in enumerate(history, 1):
        summary += f"## Session {i} — {entry['timestamp']}\n"
        if entry["added"]:
            summary += "**Added:**\n" + "\n".join(f"- {f}" for f in entry["added"]) + "\n"
        if entry["removed"]:
            summary += "**Removed:**\n" + "\n".join(f"- {f}" for f in entry["removed"]) + "\n"
        if entry["modified"]:
            summary += "**Modified:**\n" + "\n".join(f"- {f}" for f in entry["modified"]) + "\n"
        summary += "\n"
    return summary
