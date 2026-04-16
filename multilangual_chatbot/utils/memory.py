import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("data/conversation_logs.json")


def save_conversation(user, bot, lang):
    # ✅ Ensure folder exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logs = []

    # ✅ Load existing logs safely
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []

    # ✅ Append new entry
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": user,
        "bot": bot,
        "language": lang
    })

    # ✅ Save safely
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)