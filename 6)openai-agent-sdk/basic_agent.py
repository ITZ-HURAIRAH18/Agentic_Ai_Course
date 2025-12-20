from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# Try both possible environment variable names
gemini_api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

if not gemini_api_key:
    raise ValueError("API key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file")

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# System instructions for the agent
AGENT_INSTRUCTIONS = "You are an expert of agentic AI."

query = input("Enter the query: ")

try:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": AGENT_INSTRUCTIONS},
            {"role": "user", "content": query}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    if "429" in str(e) or "quota" in str(e).lower():
        print(f"⚠ Rate limit reached. Please wait a minute and try again.")
    else:
        print(f"Error: {e}")