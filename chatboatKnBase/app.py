import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en")

def load_system():
    index = faiss.read_index("vector_store/faiss.index")
    with open("vector_store/meta.pkl", "rb") as f:
        meta = pickle.load(f)
    return index, meta

def retrieve(query, index, meta, top_k=5):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)

    results = [meta["texts"][i] for i in indices[0]]
    return results

def generate_response(query, context):
    # integrate with your Gemini code here
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    return prompt  # replace with Gemini response

if __name__ == "__main__":
    index, meta = load_system()

    while True:
        query = input("User: ")
        context = retrieve(query, index, meta)
        response = generate_response(query, context)

        print("Bot:", response)