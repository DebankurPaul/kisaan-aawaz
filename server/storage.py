import httpx
import os
import base64

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

async def upload_audio(audio_bytes: bytes) -> str:
    """Upload WAV to Cloudinary, return public URL."""
    encoded = base64.b64encode(audio_bytes).decode()
    data_uri = f"data:audio/wav;base64,{encoded}"
    url = f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/auto/upload"
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            url,
            auth=(CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET),
            data={"file": data_uri, "resource_type": "auto"},
        )
        r.raise_for_status()
        return r.json()["secure_url"]