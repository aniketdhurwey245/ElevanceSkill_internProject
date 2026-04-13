import schedule
import time
from ingestion import fetch_from_website, save_raw_data
from rag.embeddings import chunk_text, embed_bge
from deduplication import remove_duplicates
from vector_updater import upsert_vectors, load_metadata

SOURCE_URL = "https://example.com"

def update_pipeline():
    print("Running scheduled update...")

    text = fetch_from_website(SOURCE_URL)
    save_raw_data(text, "web")

    chunks = chunk_text(text)

    meta = load_metadata()
    new_chunks, new_hashes = remove_duplicates(chunks, meta["hashes"])

    if not new_chunks:
        print("No new data found.")
        return

    embeddings = embed_bge(new_chunks)
    upsert_vectors(embeddings, new_chunks, new_hashes)

    print(f"Added {len(new_chunks)} new chunks.")

def start_scheduler():
    schedule.every(6).hours.do(update_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()