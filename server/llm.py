import os
from groq import AsyncGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are Kisaan Awaaz, a voice assistant for Indian farmers. Always reply in Hindi.
Write EXACTLY 2 sentences. Both sentences must be complete with a full stop.
First sentence: identify the problem. Second sentence: give one simple solution.
Never stop mid-sentence. Never write more than 2 sentences."""

async def ask_evon(question: str, context: str = "") -> str:
    client = AsyncGroq(api_key=GROQ_API_KEY)
    user_message = f"{question}\n\n[Context: {context}]" if context else question
    completion = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=300,
        temperature=0.4,
    )
    return completion.choices[0].message.content