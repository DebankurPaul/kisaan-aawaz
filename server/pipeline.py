from server.stt import transcribe
from server.tts import synthesize
from server.llm import ask_evon
from server.rag import retrieve
from server.data_feeds import get_weather, get_coords_for_phone, get_mandi_price

async def process_voice_message(audio_bytes: bytes, language: str = "hi-IN", sender: str = "") -> bytes:
    transcript = await transcribe(audio_bytes, language=language)
    print(f"[STT] {transcript}")

    # Parallel context gathering
    advisory = retrieve(transcript)
    mandi = get_mandi_price(transcript)

    lat, lon = get_coords_for_phone(sender) if sender else (26.8, 80.9)
    weather = await get_weather(lat, lon)

    context_parts = [p for p in [advisory, mandi, weather] if p]
    context = "\n".join(context_parts)
    print(f"[CTX] {context[:120]}")

    reply_text = await ask_evon(transcript, context=context)
    print(f"[LLM] {reply_text}")

    return await synthesize(reply_text, language=language)