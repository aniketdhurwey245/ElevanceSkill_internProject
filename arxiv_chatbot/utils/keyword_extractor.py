import re
from collections import Counter

STOPWORDS = {"the", "is", "and", "of", "to", "in", "for"}


def extract_keywords(texts, top_n=15):
    words = []

    for text in texts:
        tokens = re.findall(r'\b[a-z]{4,}\b', text.lower())
        words += [w for w in tokens if w not in STOPWORDS]

    return Counter(words).most_common(top_n)