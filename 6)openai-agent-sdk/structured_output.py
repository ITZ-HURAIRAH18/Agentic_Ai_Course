import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import json
import re
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_option: str

query = input("Enter the quiz topic: ")

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a quiz generator.\n"
                "Return ONLY valid JSON.\n"
                "No markdown, no explanation.\n"
                "Schema:\n"
                "{"
                "\"question\": string, "
                "\"options\": [string, string, string, string], "
                "\"correct_option\": string"
                "}"
            ),
        },
        {"role": "user", "content": query},
    ],
)

raw_output = response.choices[0].message.content.strip()

# 🔥 Extract JSON safely
match = re.search(r"\{.*\}", raw_output, re.DOTALL)
if not match:
    raise ValueError("No JSON object found in model output")

json_data = json.loads(match.group())

quiz = Quiz.model_validate(json_data)

print("\n✅ Structured Quiz Output:")
print(quiz)
