# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
print(f"[CONFIG] API key loaded: {bool(OPENAI_API_KEY)}, starts with: {OPENAI_API_KEY[:5] if OPENAI_API_KEY else 'MISSING'}")
FALLBACK_MODE = not bool(OPENAI_API_KEY)   # True when no key present
client = None
MODEL_NAME = "gpt-4o-mini"

MODEL_NAME = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)
