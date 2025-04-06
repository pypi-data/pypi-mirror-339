# tests/test_walk_project.py

import pytest
import os
from src.ai_code_review_tool.walk_project import walk_project

def test_walk_project():
    # Set up a temporary test directory structure
    test_dir = "test_project"
    os.makedirs(test_dir, exist_ok=True)

    # Create sample files
    file1 = os.path.join(test_dir, "test_file1.py")
    file2 = os.path.join(test_dir, "test_file2.html")
    file3 = os.path.join(test_dir, "other_file.txt")

    with open(file1, "w") as f:
        f.write("def sample(): pass")
    with open(file2, "w") as f:
        f.write("<html></html>")
    with open(file3, "w") as f:
        f.write("This is a test file that should be ignored.")

    # Test walking the project and getting .py and .html files
    files = walk_project(test_dir, file_extensions={".py", ".html"})
    
    # Assert the correct files are found
    assert file1 in files, f"Expected {file1} to be included."
    assert file2 in files, f"Expected {file2} to be included."
    assert file3 not in files, f"Expected {file3} to be excluded."

    # Clean up the test directory
    import shutil
    shutil.rmtree(test_dir)
