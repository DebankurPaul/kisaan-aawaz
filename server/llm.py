import httpx
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are Kisaan Awaaz, an expert agricultural advisor for Indian farmers.
Answer only in the same language the farmer used (Hindi, Bhojpuri, Marathi, or Hinglish).
Keep answers to 2-3 short spoken sentences — no bullet points, no markdown.
Focus on practical advice: crop disease, weather, mandi prices, fertilizer, irrigation.
If mandi price or weather data is provided, use it in your answer."""

async def ask_evon(question: str, context: str = "") -> str:
    """
    Send farmer question + context to Evon v3.3 (via Groq inference).
    Returns a short spoken Hindi/regional language answer.
    """
    user_message = question
    if context:
        user_message = f"{question}\n\n[Context: {context}]"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 200,
        "temperature": 0.4,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if response.status_code != 200:
            raise ValueError(f"Groq error {response.status_code}: {response.text}")
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]