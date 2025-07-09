from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import services.file_processing as file_processor
from database.crud import save_document_and_chunks, search_similar_chunks
from schemas.documents import DocumentUploadResponse, SearchResponse

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_file(
    file: UploadFile = File(..., max_size=10_000_000),  # 10 MB limit
    chunk_method: Optional[str] = "semantic",
    test_coherence: bool = Query(
        default=False,
        description="Enable semantic coherence testing (for debugging)"
    )
):
    try:
        # Process the uploaded file
        processed = await file_processor.process_uploaded_file(file, chunk_method)
        
        # Save to database
        save_result = save_document_and_chunks(
            {
                "file_name": processed["file_name"],
                "file_type": processed["file_type"],
                "file_size": processed["file_size"]
            },
            processed["chunks"],
            chunk_method
        )

       
        
        result= {
            "document_id": save_result["document_id"],
            "file_name": processed["file_name"],
            "num_chunks": save_result["num_chunks"],
            "chunking_method": chunk_method
        }
      # Conditional coherence testing
        if test_coherence:
            from tests.text_contextual_loss import test_semantic_coherence
            coherence_results = test_semantic_coherence(
                processed["original_text"],
                processed["chunks"]
            )
            print("\nSemantic Coherence Results:", coherence_results)
            result["coherence_results"]=coherence_results
        return result    
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/search", response_model=SearchResponse)
async def search_documents(query: str, top_k: Optional[int] = 5):
    try:
        results = search_similar_chunks(query, top_k)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)