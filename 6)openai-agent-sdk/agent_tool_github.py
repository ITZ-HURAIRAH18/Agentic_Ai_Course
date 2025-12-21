import os
import requests
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI  # Gemini-compatible

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def fetch_github_user(username: str) -> dict:
    """Fetch GitHub user info."""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "User not found"}
    data = response.json()
    return {
        "username": data.get("login"),
        "name": data.get("name"),
        "bio": data.get("bio"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "profile_url": data.get("html_url"),
    }

async def main():
    username = input("Enter GitHub username: ")
    user_data = fetch_github_user(username)
    print("User Data:", user_data)

    # Ask Gemini to summarize user profile
    response = await client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this GitHub profile:\n{user_data}"}
        ]
    )

    # Access content correctly
    summary = response.choices[0].message.content
    print("\nSummary:\n", summary)

asyncio.run(main())
