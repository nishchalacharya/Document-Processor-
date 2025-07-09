from pydantic import BaseModel
from typing import List, Dict, Optional

class DocumentUploadResponse(BaseModel):
    document_id: str
    file_name: str
    num_chunks: int
    chunking_method: str
    coherence_results:Optional[dict]=None

class SearchResult(BaseModel):
    chunk_text: str
    file_name: str
    similarity_score: float

class SearchResponse(BaseModel):
    query: str
    results: List[Dict]