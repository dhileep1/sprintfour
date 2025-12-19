import json
import math
from llm_client import generate_text

def generate_script(idea: str, tone: str, style: str, duration_seconds: int) -> dict:
    """
    Generates a high-retention script for a YouTube Short/Reel using Time-Based Prompting.
    """
    target_words = int(duration_seconds * 2.5)
    
    prompt = f"""
    You are an expert Content Creator for YouTube Shorts and TikTok.
    Your goal is to create a script that maximizes audience retention.

    VIDEO PARAMETERS:
    - Idea: "{idea}"
    - Tone: {tone}
    - Visual Style: {style}
    - Target Duration: {duration_seconds} seconds (~{target_words} words total)

    STRUCTURE REQUIREMENTS:
    1. Write one continuous, flowing narration script.
    2. Divide this script into logical visual scenes (approx 3-5 seconds per scene, or based on natural pauses).

    OUTPUT FORMAT:
    Return strictly valid JSON with this structure:
    {{
        "meta": {{
            "title": "Viral Video Title",
            "description": "SEO optimized description",
            "full_narration": "THE ENTIRE SCRIPT TEXT IN ONE CONTINUOUS STRING"
        }},
        "scenes": [
            {{
                "segment_text": "The specific spoken text for this visual segment.",
                "visual_prompt": "Highly detailed, cinematic prompt for AI image generator in style: {style}"
            }}
        ]
    }}
    - Output ONLY the JSON string. No markdown backticks or extra text.
    - Ensure 'full_narration' exactly matches the combined 'segment_text' of all scenes.
    """

    print(f"Generating time-based script for '{idea}' ({duration_seconds}s)...")
    response_text = generate_text(prompt)

    # Clean up output
    clean_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        script_data = json.loads(clean_text)
        if "scenes" not in script_data:
            raise ValueError("JSON missing 'scenes' key")
        return script_data
    except json.JSONDecodeError:
        print("JSON Decode Error. Raw output:\n", response_text)
        raise ValueError("LLM did not return valid JSON.")

# Test
if __name__ == "__main__":
    idea = "The secret psychology of dark mode"
    script = generate_script(idea, "Intriguing", "Minimalist Tech", 30)
    print(json.dumps(script, indent=2))