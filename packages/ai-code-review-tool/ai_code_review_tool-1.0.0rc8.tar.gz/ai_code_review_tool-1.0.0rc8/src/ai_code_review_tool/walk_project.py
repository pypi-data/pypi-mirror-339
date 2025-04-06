# walk_project.py

import os

EXCLUDED_DIRS = {"venv", ".venv", ".git", "__pycache__", ".pytest_cache", "node_modules"}

def walk_project(project_root: str = "src") -> list[str]:
    """Walk the project and return all .py files, excluding venv and cache dirs."""
    py_files = []

    for root, dirs, files in os.walk(project_root):
        # 🧹 Filter out unwanted directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                py_files.append(full_path)

    return py_files

