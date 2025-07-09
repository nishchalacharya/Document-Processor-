from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from services.embeddings import embedding_service  # Reuse your existing service

def test_semantic_coherence(original_text: str, chunks: list[str]) -> dict:
    """
    Evaluates how well chunks preserve the original text's meaning.
    
    Args:
        original_text: Complete un-chunked text
        chunks: List of generated text chunks
        
    Returns:
        {
            "avg_similarity": float (0-1),
            "problem_chunks": [(index, chunk_text, similarity)],
            "stats": {
                "min": float,
                "max": float,
                "std": float
            }
        }
    """
    # Use your existing embedding service instead of creating a new model
    orig_embed = embedding_service.generate_embedding(original_text)
    chunk_embeds = [embedding_service.generate_embedding(chunk) for chunk in chunks]
    
    # Batch similarity calculation for efficiency
    sim_matrix = cosine_similarity([orig_embed], chunk_embeds)[0]
    avg_sim = np.mean(sim_matrix)
    std_sim = np.std(sim_matrix)
    
    # Identify problematic chunks (1.5 standard deviations below mean)
    threshold = max(0.6, avg_sim - std_sim)
    problem_chunks = [
        (i, chunk[:200] + "...", round(float(sim), 3))  # Truncate long chunks
        for i, (chunk, sim) in enumerate(zip(chunks, sim_matrix))
        if sim < threshold
    ]
    
    return {
        "avg_similarity": round(float(avg_sim), 3),
        "problem_chunks": problem_chunks,
        "stats": {
            "min": round(float(np.min(sim_matrix)), 3),
            "max": round(float(np.max(sim_matrix)), 3),
            "std": round(float(std_sim), 3)
        }
    }