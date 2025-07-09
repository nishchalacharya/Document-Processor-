from datetime import datetime
from typing import List, Dict
from database.models import supabase
from services.embeddings import embedding_service

def save_document_and_chunks(file_info: Dict, chunks: List[str], chunk_method: str) -> Dict:
    # Save document metadata
    doc_data = {
        "file_name": file_info["file_name"],
        "file_type": file_info["file_type"],
        "file_size": file_info["file_size"],
        "chunking_method": chunk_method,
        "embedding_model": embedding_service.model_name
    }
    
    doc_response = supabase.table("documents").insert(doc_data).execute()
    document_id = doc_response.data[0]["id"]
    
    # Save chunks with embeddings
    chunk_records = []
    for i, chunk in enumerate(chunks):
        embedding = embedding_service.generate_embedding(chunk)
        chunk_records.append({
            "document_id": document_id,
            "chunk_text": chunk,
            "chunk_number": i + 1,
            "embedding": embedding
        })
    
    supabase.table("document_chunks").insert(chunk_records).execute()
    
    return {
        "document_id": document_id,
        "num_chunks": len(chunks)
    }

def search_similar_chunks(query: str, top_k: int = 5) -> List[Dict]:
    query_embedding = embedding_service.generate_embedding(query)
    
    # Use Supabase's vector search capability
    results = supabase.rpc("similarity_search", {
        "query_embedding": query_embedding,
        "match_threshold": 0.7,
        "match_count": top_k
    }).execute()
    
    return results.data