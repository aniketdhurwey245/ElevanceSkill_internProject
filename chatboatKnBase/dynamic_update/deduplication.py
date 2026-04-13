import hashlib

def generate_hash(text: str):
    """Generate hash for duplicate detection"""
    return hashlib.md5(text.encode()).hexdigest()

def remove_duplicates(chunks, existing_hashes: set):
    """Filter already stored chunks"""
    new_chunks = []
    new_hashes = []

    for chunk in chunks:
        h = generate_hash(chunk)
        if h not in existing_hashes:
            new_chunks.append(chunk)
            new_hashes.append(h)

    return new_chunks, new_hashes