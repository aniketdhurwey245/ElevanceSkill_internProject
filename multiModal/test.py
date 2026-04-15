from gemini_config import get_client

client = get_client()

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Explain AI simply"
)

print(response.text)