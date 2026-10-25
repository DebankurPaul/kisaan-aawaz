import httpx
import os

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"

# Voice options by language
VOICES = {
    "hi-IN": "Nalini",
    "mr-IN": "Nalini",   # update once you find Marathi voice name in Gnani catalog
    "en-IN": "Nalini",
}

async def synthesize(text: str, language: str = "hi-IN") -> bytes:
    """
    Send text to Gnani Timbre v2.5 and return WAV audio bytes.
    """
    voice = VOICES.get(language, "Nalini")
    payload = {
        "text": text,
        "voice": voice,
        "model": "timbre-v2.5",
        "language": language,
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav"
        }
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            TTS_URL,
            headers={
                "Content-Type": "application/json",
                "X-API-Key-ID": GNANI_API_KEY,
            },
            json=payload,
        )
        response.raise_for_status()
        return response.content  # raw WAV bytes