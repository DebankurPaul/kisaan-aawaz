import os
from groq import AsyncGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are Kisaan Awaaz, a voice bot for Indian farmers. Reply in the farmer's language (Hindi/Marathi/Bhojpuri).
STRICT RULES:
- Maximum 2 sentences total. Never start a 3rd sentence.
- Each sentence must be complete. Never leave a sentence unfinished.
- Speak like talking on phone — simple, direct, no percentages or measurements unless essential.
- Example good reply: "गेहूं में रस्ट रोग है। प्रोपिकोनाज़ोल दवाई का छिड़काव करें।"
"""

async def ask_evon(question: str, context: str = "") -> str:
    client = AsyncGroq(api_key=GROQ_API_KEY)
    user_message = f"{question}\n\n[Context: {context}]" if context else question
    completion = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=150,
        temperature=0.4,
    )
    return completion.choices[0].message.content