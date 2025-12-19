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
    Synchronous wrapper for generate_voice
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
             # If we are already in an event loop (e.g. maybe later in a GUI), handle differently?
             # For CLI, this usually isn't an issue.
             # But strictly, asyncio.run won't work if loop is running.
             # We'll assume simple CLI usage for now.
             asyncio.run(generate_voice(text, output_file))
        else:
             asyncio.run(generate_voice(text, output_file))
    except RuntimeError:
        # Fallback if loop issues
        asyncio.run(generate_voice(text, output_file))

if __name__ == "__main__":
    asyncio.run(generate_voice("This is a test of the audio generation system.", "test_audio.mp3"))
    print("Audio generated: test_audio.mp3")
