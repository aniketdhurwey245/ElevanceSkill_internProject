def adapt_response(text: str, lang: str) -> str:
    """
    Adjust tone based on culture/language
    """
    if lang == "hi":
        return "🙏 " + text
    elif lang == "es":
        return "😊 " + text
    elif lang == "fr":
        return "✨ " + text
    return text