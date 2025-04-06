# ai_code_review_tool/cli.py

import asyncio
import subprocess
import typer
import os
import sys
import json
import glob
import hashlib
from datetime import datetime

from ai_code_review_tool.walk_and_review_project import walk_and_review_project
from ai_code_review_tool.snapshot_tool import snapshot
from ai_code_review_tool.release import release_app
from ai_code_review_tool.generate_patches import generate_patches
from ai_code_review_tool.requirements_updater import update_requirements
from ai_code_review_tool.learning_tracker import update_learning_progress
from ai_code_review_tool.project_explainer import generate_how_it_works

cli = typer.Typer()
cli.add_typer(release_app, name="release")


@cli.command()
def review(path: str = typer.Argument("src", help="Path to the project root")):
    """Run a full code review and generate a roadmap."""
    asyncio.run(walk_and_review_project(project_root=path))


@cli.command()
def take_snapshot(tools_only: bool = False, output: str = "project_snapshot.json"):
    """Take a project snapshot."""
    snapshot(tools_only=tools_only, output=output)


@cli.command()
def generate_patches_command():
    """Generate patches from reviews."""
    generate_patches()


@cli.command(name="update-requirements")
def update_requirements_command():
    """Auto-generate requirements.txt based on current imports."""
    update_requirements()


@cli.command()
def generate_docs(
    output: str = "docs/cli_commands.md",
    update_readme: bool = True,
    version: str = "v1.0.0"
):
    """
    Generate CLI docs automatically from the typer app.
    Saves to both docs/cli_commands.md and optionally updates README.md.
    """
    import toml
    from pathlib import Path

    os.makedirs(os.path.dirname(output), exist_ok=True)
    python_exe = sys.executable
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 📦 Read pyproject.toml for metadata
    pyproject = toml.loads(Path("pyproject.toml").read_text())
    version = pyproject["project"]["version"]
    package_name = pyproject["project"]["name"]

    header = f"# 🧠 AI Code Review Tool – CLI Commands\n\n" \
             f"**Version:** `{version}`  \n" \
             f"**Last updated:** `{timestamp}`\n\n---\n"

    cli_sections = []
    main_help = subprocess.run(
        [python_exe, "-m", "ai_code_review_tool.cli", "--help"],
        capture_output=True, text=True, check=True
    ).stdout
    cli_sections.append(("main", main_help))

    subcommands = ["review", "take-snapshot", "generate-docs", "generate-patches", "update-requirements", "release"]
    for cmd in subcommands:
        try:
            help_output = subprocess.run(
                [python_exe, "-m", "ai_code_review_tool.cli", cmd, "--help"],
                capture_output=True, text=True, check=True
            ).stdout
            cli_sections.append((cmd, help_output))
        except subprocess.CalledProcessError:
            cli_sections.append((cmd, f"❌ Failed to get help for `{cmd}`"))

    full_md = header
    for name, help_text in cli_sections:
        section_title = f"## `{name}` command\n\n" if name != "main" else "## 🧰 Main CLI\n\n"
        full_md += section_title
        full_md += "```\n" + help_text.strip() + "\n```\n\n"

    # 🔍 File change detection
    cache_file = "docs/.last_docs_gen.json"
    tracked_files = glob.glob("src/**/*.py", recursive=True)
    current = {
        f: hashlib.sha1(open(f, "rb").read()).hexdigest()
        for f in tracked_files if os.path.exists(f)
    }

    previous = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            previous = json.load(f)

    added = sorted(set(current) - set(previous))
    removed = sorted(set(previous) - set(current))
    modified = sorted(f for f in current if f in previous and current[f] != previous[f])

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)

    changes_section = "## 🧾 Changes Since Last CLI Docs\n\n"
    if added:
        changes_section += "**➕ Added:**\n" + "\n".join(f"- {f}" for f in added) + "\n"
    if removed:
        changes_section += "**➖ Removed:**\n" + "\n".join(f"- {f}" for f in removed) + "\n"
    if modified:
        changes_section += "**✏️ Modified:**\n" + "\n".join(f"- {f}" for f in modified) + "\n"
    changes_section += "\n"
    full_md += changes_section

    # 🧠 Learning progress
    full_md += update_learning_progress({
        "added": added,
        "removed": removed,
        "modified": modified
    })

    # 🧩 Project summary
    full_md += generate_how_it_works()

    # 🚀 Dynamic release instructions
    release_block = f"""
## 🚀 Release & Publish Instructions

- [ ] Run `python -m ai_code_review_tool.cli release prerelease --bump rc`
- [ ] Run `python -m ai_code_review_tool.cli release prepare --bump rc`
- [ ] Run `python -m ai_code_review_tool.cli release publish`
- [ ] Push with `git push --follow-tags`
- [ ] Verify on PyPI: [{package_name} v{version}](https://pypi.org/project/{package_name}/{version}/)
"""
    full_md += release_block

    # 💾 Write to markdown
    with open(output, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"✅ CLI docs saved to {output}")

    # 📘 Update README.md
    project_root = Path(__file__).resolve().parents[1]
    readme_path = project_root / "README.md"

    if update_readme and readme_path.exists():
        lines = readme_path.read_text(encoding="utf-8").splitlines(keepends=True)

        start_marker = "<!-- CLI-DOCS-START -->"
        end_marker = "<!-- CLI-DOCS-END -->"
        start = next((i for i, line in enumerate(lines) if start_marker in line), None)
        end = next((i for i, line in enumerate(lines) if end_marker in line), None)

        if start is not None and end is not None:
            new_readme = lines[:start+1] + ["\n" + full_md + "\n"] + lines[end:]
            readme_path.write_text("".join(new_readme), encoding="utf-8")
            print("✅ README.md updated with CLI docs.")
        else:
            print("⚠️ README.md missing CLI-DOCS markers.")



if __name__ == "__main__":
    cli()
