import httpx
import os

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BASE_URL = "https://graph.facebook.com/v19.0"

async def download_audio(media_id: str) -> bytes:
    """Download OGG audio from Meta CDN using media_id."""
    async with httpx.AsyncClient(timeout=30) as client:
        # Step 1: Get download URL
        r = await client.get(
            f"{BASE_URL}/{media_id}",
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
        )
        r.raise_for_status()
        download_url = r.json()["url"]

        # Step 2: Download the actual audio
        r2 = await client.get(
            download_url,
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
        )
        r2.raise_for_status()
        return r2.content

async def send_audio_reply(to: str, audio_bytes: bytes) -> dict:
    """Upload WAV and send as voice note to WhatsApp number."""
    async with httpx.AsyncClient(timeout=60) as client:
        # Step 1: Upload audio to Meta
        upload = await client.post(
            f"{BASE_URL}/{PHONE_NUMBER_ID}/media",
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
            files={"file": ("reply.wav", audio_bytes, "audio/wav")},
            data={"messaging_product": "whatsapp"},
        )
        upload.raise_for_status()
        media_id = upload.json()["id"]

        # Step 2: Send audio message
        send = await client.post(
            f"{BASE_URL}/{PHONE_NUMBER_ID}/messages",
            headers={
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "audio",
                "audio": {"id": media_id},
            },
        )
        send.raise_for_status()
        return send.json()