import asyncio
import edge_tts
import os

async def generate_voice(text: str, output_file: str, voice: str = "en-US-ChristopherNeural") -> None:
    """
    Generates audio file from text using Edge TTS.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def generate_audio_sync(text: str, output_file: str):
    """
    Synchronous wrapper for generate_voice. Uses existing loop if available.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        import threading
        # Run in a separate thread to avoid blocking or loop conflicts
        thread = threading.Thread(target=lambda: asyncio.run(generate_voice(text, output_file)))
        thread.start()
        thread.join()
    else:
        loop.run_until_complete(generate_voice(text, output_file))

if __name__ == "__main__":
    asyncio.run(generate_voice("This is a test of the audio generation system.", "test_audio.mp3"))
    print("Audio generated: test_audio.mp3")
