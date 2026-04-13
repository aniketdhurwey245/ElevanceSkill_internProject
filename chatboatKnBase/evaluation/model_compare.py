from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieval_accuracy(query_vec, doc_vectors, top_k=5):
    sims = cosine_similarity([query_vec], doc_vectors)[0]
    top_indices = np.argsort(sims)[-top_k:]
    return top_indices

def mean_reciprocal_rank(ranks):
    return np.mean([1/r for r in ranks if r > 0])