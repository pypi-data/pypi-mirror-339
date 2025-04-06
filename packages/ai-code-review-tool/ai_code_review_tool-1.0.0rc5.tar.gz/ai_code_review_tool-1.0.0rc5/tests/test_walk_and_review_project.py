import pytest
from unittest import mock
from src.ai_code_review_tool.walk_and_review_project import walk_and_review_project


@pytest.mark.asyncio
async def test_walk_and_review_project():
    """Test if walking through the project and generating feedback works as expected."""
    project_root = "./"  # Update this to the actual path of your project directory

    # Mocking the OpenAI API response
    mock_response = mock.Mock()
    mock_response.choices = [mock.Mock(text="Refactor complex functions.")]

    # Mocking the get_code_review_suggestions function
    with mock.patch('src.ai_code_review_tool.walk_and_review_project.get_code_review_suggestions', return_value="Refactor complex functions."):
        feedbacks, roadmap = await walk_and_review_project(project_root)

    # Check if feedback is generated
    assert len(feedbacks) > 0, "Expected feedback from the code review"

    # Check if roadmap is generated
    assert len(roadmap) > 0, "Expected roadmap from the code review"
