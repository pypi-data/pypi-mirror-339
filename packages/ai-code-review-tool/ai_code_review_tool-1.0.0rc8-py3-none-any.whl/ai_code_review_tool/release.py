import subprocess
import sys
import typer
from ai_code_review_tool.version_utils import bump_version, get_project_version, set_project_version
from ai_code_review_tool.git_utils import get_changed_files, generate_commit_message, commit_and_push

release_app = typer.Typer()

@release_app.command("prepare")
def prepare_release(bump: str = typer.Option(..., help="Version bump type: patch, minor, major, rc")):
    """
    Prepare a new release: bump version, update files, and show next version.
    """
    current = get_project_version()
    new_version = bump_version(current, bump)
    set_project_version(new_version)
    print(f"✅ Version bumped from {current} → {new_version}")

    changed_files = get_changed_files()
    print("📄 Changed files since last commit:")
    for f in changed_files:
        print(f" - {f}")

    commit_msg = generate_commit_message(changed_files)
    print("\n📜 Suggested commit message:\n")
    print(commit_msg)

    confirm = typer.confirm("Do you want to commit and push these changes?")
    if confirm:
        commit_and_push(commit_msg)
        print("🚀 Changes committed and pushed.")

@release_app.command("publish")
def publish_to_pypi():
    """
    Build and publish the current version to PyPI.
    """
    print("📦 Building wheel and source distribution...")
    subprocess.run([sys.executable, "-m", "build"], check=True)

    print("🚀 Uploading to PyPI...")
    subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"], check=True)

    print("✅ Publish complete.")

@release_app.command("prerelease")
def prerelease_workflow(bump: str = typer.Option("rc", help="Bump type for prerelease")):
    """
    Automate pre-release steps before versioning and publishing.
    """
    print("🔁 Running pre-release automation...")

    subprocess.run([sys.executable, "-m", "ai_code_review_tool.cli", "generate-docs"], check=True)
    subprocess.run([sys.executable, "-m", "ai_code_review_tool.cli", "update-requirements"], check=True)
    subprocess.run([sys.executable, "-m", "ai_code_review_tool.cli", "take-snapshot"], check=True)

    print("🧼 Pre-release tasks complete. Run `python main.py release prepare --bump rc` to finalize.")
