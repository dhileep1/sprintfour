import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("KEY")

if not GOOGLE_API_KEY:
    raise ValueError("KEY not found in .env file. Please ensure it is set.")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent"


CF_KEY = os.getenv("CF_KEY")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
GROQ_API_KEY = os.getenv("GROQ")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IMG_ROUTER = os.getenv("IMG_ROUTER")
RUNWARE_API_KEY = os.getenv("RUNWARE")
SD_LOCAL_URL = "http://127.0.0.1:7860"

