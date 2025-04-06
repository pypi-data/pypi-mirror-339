from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

async def get_code_review_suggestions(code: str, role: str) -> str:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful AI code reviewer for the {role} role."},
                {"role": "user", "content": code}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "An error occurred while fetching suggestions from OpenAI."
