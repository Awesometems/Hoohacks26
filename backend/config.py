# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
FALLBACK_MODE = not bool(OPENAI_API_KEY)   # True when no key present

client = None
MODEL_NAME = "gpt-4o-mini"

if not FALLBACK_MODE:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)