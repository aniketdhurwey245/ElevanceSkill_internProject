import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

# Load model
model = SentenceTransformer("BAAI/bge-small-en")

# Sample data (you can replace later)
texts = [
"Artificial Intelligence (AI) is the simulation of human intelligence in machines.",
"Machine Learning (ML) is a subset of AI that enables systems to learn from data.",
"Deep Learning is a subset of ML that uses neural networks with many layers.",
"Natural Language Processing (NLP) allows machines to understand human language.",
"Computer Vision enables machines to interpret and understand visual information.",

"Google is a multinational technology company specializing in Internet-related services.",
"The CEO of Google is Sundar Pichai.",
"Sundar Pichai became CEO of Google in 2015.",
"Google is owned by Alphabet Inc.",

"Microsoft is a technology company founded by Bill Gates.",
"The CEO of Microsoft is Satya Nadella.",

"Apple Inc. is a technology company known for iPhones and Mac computers.",
"The CEO of Apple is Tim Cook.",

"Python is a high-level programming language used for AI and data science.",
"Java is a widely used programming language for enterprise applications.",
"C++ is used for system-level programming.",

"A chatbot is a software application that simulates human conversation.",
"Chatbots use NLP and machine learning techniques.",
"RAG stands for Retrieval-Augmented Generation."

]

# Convert to embeddings
embeddings = model.encode(texts).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add data
index.add(embeddings)

# Save index
os.makedirs("vector_store", exist_ok=True)
faiss.write_index(index, "vector_store/faiss.index")

# Save metadata
meta = {
    "texts": texts
}

with open("vector_store/meta.pkl", "wb") as f:
    pickle.dump(meta, f)

print("✅ FAISS index created successfully!")