# src/ai_code_review_tool/walk_project.py

import os

def walk_project(root_dir=".", file_extensions={".py", ".html", ".css"}):
    """Walks through a project directory and collects all files with the specified extensions."""
    files = []
    print(f"Walking through directory: {root_dir}")  # Debugging line
    for root, dirs, filenames in os.walk(root_dir):
        print(f"Scanning directory: {root}")  # Debugging line
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_extensions):
                files.append(os.path.join(root, filename))
    print(f"Found files: {files}")  # Debugging line
    return files
