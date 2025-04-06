# tests/test_generate_roadmap.py

import pytest
from src.ai_code_review_tool.generate_roadmap import generate_roadmap


def test_generate_roadmap():
    feedback = "Refactor the code and add missing tests."
    roadmap = generate_roadmap(feedback)
    assert "Refactor" in roadmap[0], "Expected roadmap to include refactor steps."
    assert "Write unit tests" in roadmap[1], "Expected roadmap to include test writing."
