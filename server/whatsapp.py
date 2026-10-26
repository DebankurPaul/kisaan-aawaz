import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+17372508034")

def send_audio_reply_twilio(to: str, audio_url: str) -> dict:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    to_number = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
    msg = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to_number,
        media_url=[audio_url],
    )
    return {"sid": msg.sid}