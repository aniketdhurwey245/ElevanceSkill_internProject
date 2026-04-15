import requests

OLLAMA_API = "http://localhost:11434/api/generate"


def call_ollama(prompt: str, model="llama3") -> str:
    try:
        res = requests.post(OLLAMA_API, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=60)

        if res.status_code == 200:
            return res.json().get("response", "")
    except:
        return None


def generate_answer(query, papers, history):
    context = ""

    for i, p in enumerate(papers[:3], 1):
        context += f"[{i}] {p.title}\n{p.abstract[:300]}\n\n"

    prompt = f"""
You are an AI Research Expert.

Context:
{context}

User Question:
{query}

Instructions:
- Explain clearly
- Use examples
- Reference papers if relevant
"""

    result = call_ollama(prompt)

    if result:
        return result

    return "⚠️ LLM not available. Showing papers only."