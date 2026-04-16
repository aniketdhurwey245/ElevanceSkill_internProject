import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(prompt: str, model="llama3"):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        if response.status_code == 200:
            return response.json().get("response", "")
    except:
        pass

    # fallback
    return "I'm here to help. Could you please clarify your question?"