from groq import Groq
import json
from config import GROQ_API_KEY

def generate_text(prompt: str) -> str:
    """
    Generates text using Groq API.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=16382,
            top_p=1,
            stream=False,
            stop=None
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Groq API Request Failed: {e}")
        raise
