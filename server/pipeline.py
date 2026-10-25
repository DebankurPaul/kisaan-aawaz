from server.stt import transcribe
from server.tts import synthesize
from server.llm import ask_evon

async def process_voice_message(audio_bytes: bytes, language: str = "hi-IN") -> bytes:
    """
    Full pipeline: OGG audio bytes in → WAV audio bytes out
    1. Transcribe with Prisma STT
    2. Get crop advice from Evon LLM
    3. Synthesize reply with Timbre TTS
    """
    # Step 1: Speech to text
    transcript = await transcribe(audio_bytes, language=language)
    print(f"[STT] Transcript: {transcript}")

    # Step 2: LLM response
    reply_text = await ask_evon(transcript)
    print(f"[LLM] Reply: {reply_text}")

    # Step 3: Text to speech
    reply_audio = await synthesize(reply_text, language=language)
    print(f"[TTS] Audio size: {len(reply_audio)} bytes")

    return reply_audio