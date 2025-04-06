import pytest
from unittest.mock import AsyncMock, patch

from src.ai_code_review_tool.get_code_review_suggestions import get_code_review_suggestions

@pytest.mark.asyncio
async def test_get_code_review_suggestions_success():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value.choices = [
        type("Choice", (), {
            "message": type("Message", (), {"content": "The function is simple and clear. No major changes needed."})()
        })()
    ]

    with patch("src.ai_code_review_tool.get_code_review_suggestions.AsyncOpenAI", return_value=mock_client):
        feedback = await get_code_review_suggestions("def foo(): pass", "Backend")

    assert "simple" in feedback
