import httpx
import os

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
STT_URL = "https://api.vachana.ai/stt/v3"

async def transcribe(audio_bytes: bytes, language: str = "hi-IN") -> str:
    """
    Send audio bytes to Gnani Prisma v2.5 and return transcript.
    language options: hi-IN, mr-IN, bn-IN, pa-IN, en-IN
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            STT_URL,
            headers={"X-API-Key-ID": GNANI_API_KEY},
            files={"audio_file": ("audio.ogg", audio_bytes, "audio/ogg")},
            data={"language_code": language, "format": "transcribe"},
        )
        response.raise_for_status()
        result = response.json()
        if not result.get("success"):
            raise ValueError(f"STT failed: {result}")
        return result["transcript"]