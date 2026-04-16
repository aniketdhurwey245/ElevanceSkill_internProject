import requests

OLLAMA_API = "http://localhost:11434/api/generate"

class AdvancedResponseGenerator:

    def generate(self, query, emotion_data, history):
        tone = self._tone_map(emotion_data)

        context = "\n".join([f"{h['role']}: {h['content']}" for h in history])

        prompt = f"""
You are an advanced emotional AI assistant.

User Emotion: {emotion_data['emotion']}
Intensity: {emotion_data['intensity']}

Conversation Context:
{context}

Instruction:
{tone}

User Query:
{query}

Respond intelligently.
"""

        try:
            res = requests.post(OLLAMA_API, json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            })
            return res.json().get("response", "")
        except:
            return "⚠️ AI backend unavailable."

    def _tone_map(self, emotion):
        e = emotion["emotion"]

        if e in ["sadness", "anger"]:
            return "Be empathetic, calm, and supportive."
        elif e == "joy":
            return "Be enthusiastic and engaging."
        else:
            return "Be professional and helpful."