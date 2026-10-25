from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Kisaan Awaaz is live"}

@app.get("/health")
def health():
    return {"status": "ok"}

# WhatsApp webhook verification
@app.get("/webhook")
def verify_webhook(request: Request):
    params = dict(request.query_params)
    token = params.get("hub.verify_token", "")
    challenge = params.get("hub.challenge", "")
    if token == os.getenv("WEBHOOK_VERIFY_TOKEN", "kisaan123"):
        return int(challenge)
    return {"error": "Invalid token"}

# WhatsApp message handler (will be filled tomorrow)
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    return {"status": "received"}

@app.get("/test-stt")
async def test_stt():
    # We'll test with a real audio file tomorrow
    return {"message": "STT ready - send audio via POST /webhook"}

@app.get("/test-tts")  
async def test_tts():
    from server.tts import synthesize
    wav_bytes = await synthesize("नमस्ते किसान भाई, आपकी फसल की जानकारी दें।")
    return {"size_bytes": len(wav_bytes), "status": "Timbre working"}