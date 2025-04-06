# tests/test_chunk_file.py

import pytest
from src.ai_code_review_tool.chunk_file import chunk_file

def test_chunk_file():
    # Sample input file content (simulating a file as a string)
    test_file_content = "Line " + "\nLine ".join(str(i) for i in range(1, 101))

    # Save it to a test file
    test_file_path = "test_file.txt"
    with open(test_file_path, "w", encoding="utf-8") as file:
        file.write(test_file_content)

    # Test chunking with a chunk size of 20 lines
    chunks = chunk_file(test_file_path, chunk_size=20)

    # Check if chunks are correctly split
    assert len(chunks) == 5, f"Expected 5 chunks, got {len(chunks)}"
    assert len(chunks[0].splitlines()) == 20, f"Expected chunk size of 20 lines, got {len(chunks[0].splitlines())}"
    assert len(chunks[-1].splitlines()) == 20, f"Expected chunk size of 20 lines, got {len(chunks[-1].splitlines())}"

    # Clean up test file
    import os
    os.remove(test_file_path)
