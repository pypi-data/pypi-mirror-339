# tools/ai_code_review/snapshot_tool.py

import os
import json
from pathlib import Path
import typer

app = typer.Typer()

ALLOWED_EXTENSIONS = {'.py', '.html', '.css'}
IGNORED_DIRS = {"venv", "__pycache__", ".git"}
SNAPSHOT_FILE = "project_snapshot.json"

def is_valid_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def walk_project(root=".", tools_only=False):
    project_snapshot = {"files": []}
    root_path = Path(root)
    scan_path = root_path / "tools" if tools_only else root_path

    for folder in scan_path.rglob("*"):
        if folder.is_dir() and any(part in IGNORED_DIRS for part in folder.parts):
            continue
        for f in folder.glob("*"):
            if f.is_file() and is_valid_file(f.name):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    project_snapshot["files"].append({
                        "path": str(f.relative_to(root_path)),
                        "content": content
                    })
                except Exception:
                    continue  # Skip unreadable files
    return project_snapshot

def save_snapshot(snapshot, path=SNAPSHOT_FILE):
    with open(path, "w", encoding="utf-8") as out:
        json.dump(snapshot, out, indent=2)
    print(f"✅ Snapshot saved to {path}")

@app.command()
def snapshot(
    tools_only: bool = typer.Option(False, "--tools-only", help="Only scan the tools/ directory."),
    output: str = typer.Option(SNAPSHOT_FILE, "--output", "-o", help="Path to save the snapshot JSON.")
):
    """
    Generate a project snapshot of code files for AI review.
    """
    print("📁 Scanning project...")
    snapshot = walk_project(".", tools_only=tools_only)
    save_snapshot(snapshot, path=output)

if __name__ == "__main__":
    app()
