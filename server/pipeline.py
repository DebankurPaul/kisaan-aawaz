from server.stt import transcribe
from server.tts import synthesize
from server.llm import ask_evon
from server.rag import retrieve

async def process_voice_message(audio_bytes: bytes, language: str = "hi-IN") -> bytes:
    # Step 1: Speech to text
    transcript = await transcribe(audio_bytes, language=language)
    print(f"[STT] Transcript: {transcript}")

    # Step 2: Retrieve relevant advisories
    context = retrieve(transcript)
    print(f"[RAG] Context: {context[:100]}...")

    # Step 3: LLM response with context
    reply_text = await ask_evon(transcript, context=context)
    print(f"[LLM] Reply: {reply_text}")

    # Step 4: Text to speech
    reply_audio = await synthesize(reply_text, language=language)
    return reply_audio