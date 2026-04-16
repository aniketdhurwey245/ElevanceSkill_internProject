import re
from datetime import datetime


def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def truncate_text(text: str, max_len: int = 200) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def format_time() -> str:
    return datetime.now().strftime("%H:%M")


def safe_get(d: dict, key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default