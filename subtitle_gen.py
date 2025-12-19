import os
import requests
import json
from config import GROQ_API_KEY

def format_timestamp(seconds: float):
    """Converts seconds into SRT timestamp format HH:MM:SS,mmm"""
    td_ms = int((seconds % 1) * 1000)
    td_sec = int(seconds) % 60
    td_min = (int(seconds) // 60) % 60
    td_hr = int(seconds) // 3600
    return f"{td_hr:02}:{td_min:02}:{td_sec:02},{td_ms:03}"

def generate_subtitles(audio_path: str, output_srt_path: str):
    """
    Transcribes audio using Groq's Whisper API and manually converts JSON to SRT.
    This bypasses the missing 'srt' format support in Groq's current API.
    """
    print(f"Transcribing audio for subtitles (Groq Whisper)...")
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    try:
        with open(audio_path, "rb") as f:
            files = {
                "file": (os.path.basename(audio_path), f),
                "model": (None, "whisper-large-v3"),
                "response_format": (None, "verbose_json")
            }
            response = requests.post(url, headers=headers, files=files)
            
        if response.status_code != 200:
            print(f"Groq Subtitle Error {response.status_code}: {response.text}")
            return False

        data = response.json()
        segments = data.get("segments", [])
        
        srt_content = ""
        for i, segment in enumerate(segments):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            srt_content += f"{i + 1}\n{start} --> {end}\n{text}\n\n"

        with open(output_srt_path, "w", encoding="utf-8") as srt_file:
            srt_file.write(srt_content)
            
        print(f"Subtitles generated and converted to SRT.")
        return True
    except Exception as e:
        print(f"Groq Subtitle generation failed: {e}")
        return False

if __name__ == "__main__":
    # Test
    generate_subtitles("output/master_audio.mp3", "output/subtitles.srt")
