from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# Advanced Model
bge_model = SentenceTransformer("BAAI/bge-small-en")

# Baseline Model
tfidf_vectorizer = TfidfVectorizer()

def chunk_text(text, chunk_size=300, overlap=50):
    """Split text into overlapping chunks"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks

def embed_bge(chunks):
    """Advanced embeddings"""
    return bge_model.encode(chunks)

def embed_tfidf(chunks):
    """Baseline embeddings"""
    return tfidf_vectorizer.fit_transform(chunks)