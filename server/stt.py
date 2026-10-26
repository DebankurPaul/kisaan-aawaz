import httpx
import os
import subprocess
import tempfile

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
STT_URL = "https://api.vachana.ai/stt/v3"

async def transcribe(audio_bytes: bytes, language: str = "hi-IN") -> str:
    # Convert to 16kHz mono WAV using ffmpeg
    try:
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
            f.write(audio_bytes)
            input_path = f.name
        output_path = input_path.replace(".ogg", ".wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1", "-sample_fmt", "s16",
            output_path
        ], capture_output=True, check=True)
        with open(output_path, "rb") as f:
            wav_bytes = f.read()
        os.unlink(input_path)
        os.unlink(output_path)
    except Exception as e:
        print(f"[STT] ffmpeg conversion failed: {e}, sending raw")
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