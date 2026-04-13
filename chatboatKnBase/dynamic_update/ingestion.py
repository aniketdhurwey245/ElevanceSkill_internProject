import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

DATA_DIR = "data/raw"

def fetch_from_api(api_url: str):
    """Fetch data from API"""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_from_website(url: str):
    """Scrape text from website"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    return "\n".join(paragraphs)

def save_raw_data(content: str, source: str):
    """Save raw text with timestamp"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"{source}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)

    return filename