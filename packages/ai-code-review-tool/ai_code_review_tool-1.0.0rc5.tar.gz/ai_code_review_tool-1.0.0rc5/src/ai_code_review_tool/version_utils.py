# src/ai_code_review_tool/version_utils.py

import toml
import re

PYPROJECT_FILE = "pyproject.toml"

def get_project_version() -> str:
    """
    Extracts the current version from pyproject.toml.
    """
    with open(PYPROJECT_FILE, "r", encoding="utf-8") as f:
        data = toml.load(f)
    return data["project"]["version"]

def set_project_version(new_version: str):
    """
    Updates the version field in pyproject.toml.
    """
    with open(PYPROJECT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(PYPROJECT_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip().startswith("version ="):
                f.write(f'version = "{new_version}"\n')
            else:
                f.write(line)

def bump_version(version: str, part: str = "rc") -> str:
    """
    Bumps the version based on the specified part (major, minor, patch, rc).
    """
    major, minor, patch = parse_version(version)
    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    elif part == "rc":
        rc_match = re.match(r"(.*?)(?:-rc(\d+))?$", version)
        base, rc_num = rc_match.groups()
        rc_num = int(rc_num or 0) + 1
        return f"{base}-rc{rc_num}"
    return version  # fallback

def parse_version(version: str):
    base = version.split("-")[0]
    major, minor, patch = map(int, base.split("."))
    return major, minor, patch
