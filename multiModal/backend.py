from gemini_config import get_client

client = get_client()

def get_text_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def get_image_response(image, prompt):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=[prompt, image]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"