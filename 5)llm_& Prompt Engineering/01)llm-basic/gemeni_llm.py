from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY` or GOOGLE_API_KEY
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))

# Using the latest Gemini 2.5 Flash model
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="What is the capital of Pakistan?"
)

print(response.text)