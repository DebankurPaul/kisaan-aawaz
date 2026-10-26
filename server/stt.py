import httpx
import os
import io
from pydub import AudioSegment

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
STT_URL = "https://api.vachana.ai/stt/v3"

async def transcribe(audio_bytes: bytes, language: str = "hi-IN") -> str:
    # Convert to 16kHz mono WAV — Gnani requirement
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_bytes = wav_buffer.getvalue()
    except Exception as e:
        print(f"[STT] Audio conversion failed: {e}, sending raw")
        wav_bytes = audio_bytes

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            STT_URL,
            headers={"X-API-Key-ID": GNANI_API_KEY},
            files={"audio_file": ("audio.wav", wav_bytes, "audio/wav")},
            data={"language_code": language, "format": "transcribe"},
        )
        response.raise_for_status()
        result = response.json()
        if not result.get("success"):
            raise ValueError(f"STT failed: {result}")
        return result["transcript"]