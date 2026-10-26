from fastapi import FastAPI, Request
import os

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
@app.get("/")
def root():
    return {"status": "Kisaan Awaaz is live"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhook")
def verify_webhook(request: Request):
    params = dict(request.query_params)
    token = params.get("hub.verify_token", "")
    challenge = params.get("hub.challenge", "")
    # Meta verification
    if token == os.getenv("WEBHOOK_VERIFY_TOKEN", "kisaan123"):
        return int(challenge)
    # Twilio just does a GET check — return 200
    return {"status": "ok"}

@app.post("/webhook")
async def receive_message(request: Request):
    from server.pipeline import process_voice_message
    from server.storage import upload_audio
    form = await request.form()
    sender = form.get("From", "")
    num_media = int(form.get("NumMedia", 0))
    if num_media == 0:
        return {"status": "no media"}
    media_url = form.get("MediaUrl0", "")
    media_type = form.get("MediaContentType0", "")
    # Download audio from Twilio
    import httpx, base64
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            media_url,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        )
        audio_bytes = r.content
    reply_audio = await process_voice_message(audio_bytes, sender=sender)
    public_url = await upload_audio(reply_audio)
    from server.whatsapp import send_audio_reply_twilio
    send_audio_reply_twilio(sender, public_url)
    return {"status": "replied"}

@app.get("/test-tts")
async def test_tts():
    from server.tts import synthesize
    wav_bytes = await synthesize("नमस्ते किसान भाई, आपकी फसल की जानकारी दें।")
    return {"size_bytes": len(wav_bytes), "status": "Timbre working"}

@app.get("/test-llm")
async def test_llm():
    try:
        from server.llm import ask_evon
        reply = await ask_evon("गेहूं की फसल में पीले धब्बे आ रहे हैं, क्या करूं?")
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-pipeline")
async def test_pipeline():
    from server.llm import ask_evon
    from server.tts import synthesize
    from server.rag import retrieve
    query = "गेहूं में पीले धब्बे आ रहे हैं"
    context = retrieve(query)
    reply_text = await ask_evon(query, context=context)
    audio = await synthesize(reply_text)
    return {"text": reply_text, "audio_bytes": len(audio), "context_found": bool(context)}

@app.get("/test-weather")
async def test_weather():
    from server.data_feeds import get_weather
    result = await get_weather(30.9, 75.8)  # Ludhiana
    return {"weather": result}