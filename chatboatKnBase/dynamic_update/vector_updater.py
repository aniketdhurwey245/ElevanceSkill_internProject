import faiss
import numpy as np
import os
import pickle

VECTOR_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/meta.pkl"

def load_index(dim=384):
    if os.path.exists(VECTOR_PATH):
        return faiss.read_index(VECTOR_PATH)
    return faiss.IndexFlatL2(dim)

def save_index(index):
    faiss.write_index(index, VECTOR_PATH)

def load_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH, "rb") as f:
            return pickle.load(f)
    return {"texts": [], "hashes": set()}

def save_metadata(meta):
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

def upsert_vectors(embeddings, texts, hashes):
    index = load_index(len(embeddings[0]))
    meta = load_metadata()

    index.add(np.array(embeddings).astype("float32"))

    meta["texts"].extend(texts)
    meta["hashes"].update(hashes)

    save_index(index)
    save_metadata(meta)