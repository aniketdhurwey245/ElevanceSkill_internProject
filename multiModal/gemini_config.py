from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("API key not found")

    return genai.Client(api_key=api_key)