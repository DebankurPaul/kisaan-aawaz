import os
from groq import AsyncGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are Kisaan Awaaz, an expert agricultural advisor for Indian farmers.
Answer only in the same language the farmer used (Hindi, Bhojpuri, Marathi, or Hinglish).
Keep answers to 2-3 SHORT complete sentences — always finish the last sentence fully.
No bullet points, no markdown, no incomplete sentences.
Focus on: crop disease, weather, mandi prices, fertilizer, irrigation."""

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