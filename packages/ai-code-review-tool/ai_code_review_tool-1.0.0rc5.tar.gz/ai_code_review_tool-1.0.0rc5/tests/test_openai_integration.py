from unittest import mock
from src.ai_code_review_tool.openai_integration import get_openai_response

def test_openai_response():
    """Test OpenAI integration to ensure the response is correct."""
    prompt = "What is the capital of France?"

    # Build mock object with correct attribute access
    mock_message = mock.Mock()
    mock_message.content = "Paris"

    mock_choice = mock.Mock()
    mock_choice.message = mock_message

    mock_response = mock.Mock()
    mock_response.choices = [mock_choice]

    # Patch OpenAI client inside the module
    with mock.patch("src.ai_code_review_tool.openai_integration.OpenAI") as MockOpenAI:
        instance = MockOpenAI.return_value
        instance.chat.completions.create.return_value = mock_response

        response = get_openai_response(prompt)

    assert response is not None, "Expected a response from OpenAI, but received None."
    assert "Paris" in response
