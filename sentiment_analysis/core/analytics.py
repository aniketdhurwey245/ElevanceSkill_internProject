import json
from datetime import datetime

LOG_FILE = "data/logs.json"

def log_interaction(query, emotion):
    data = []

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        pass

    data.append({
        "time": str(datetime.now()),
        "query": query,
        "emotion": emotion["emotion"],
        "intensity": emotion["intensity"]
    })

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)