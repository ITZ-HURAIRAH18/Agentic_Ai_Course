import asyncio
import uuid
import os
from dotenv import load_dotenv

from openai import AsyncOpenAI
from openai.types.responses import (
    ResponseTextDeltaEvent,
    ResponseContentPartDoneEvent,
)

from agents import (
    Agent,
    Runner,
    RawResponsesStreamEvent,
    TResponseInputItem,
    trace,
)
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel


# ===============================
# ENV
# ===============================
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing")


# ===============================
# GEMINI CLIENT (OpenAI compatible)
# ===============================
openai_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# ===============================
# AGENTS
# ===============================
french_agent = Agent(
    name="french_agent",
    instructions="You only speak French.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=openai_client,
    ),
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=openai_client,
    ),
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=openai_client,
    ),
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Detect language and handoff to correct agent.",
    handoffs=[french_agent, spanish_agent, english_agent],
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=openai_client,
    ),
)


# ===============================
# MAIN
# ===============================
async def main():
    conversation_id = uuid.uuid4().hex[:16]

    print("🌍 Hi! We support French, Spanish & English.")
    print("Type 'exit' to quit.\n")

    first_msg = input("You: ").strip()

    inputs: list[TResponseInputItem] = [
        {"role": "user", "content": first_msg}
    ]

    current_agent = triage_agent

    while True:
        with trace("language-routing", group_id=conversation_id):
            result = Runner.run_streamed(
                current_agent,
                input=inputs,
            )

            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue

                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print()

        # ✅ HISTORY IS PRESERVED HERE
        inputs = result.to_input_list()

        current_agent = result.current_agent
        print(f"\n🧠 Current Agent: {current_agent.name}")

        user_msg = input("\nYou: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        inputs.append({"role": "user", "content": user_msg})


if __name__ == "__main__":
    asyncio.run(main())
