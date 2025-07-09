import os
from typing import Union
from pypdf import PdfReader
from fastapi import UploadFile
from .chunking import semantic_chunking
import io

async def process_uploaded_file(file: UploadFile, chunk_method: str = "semantic"):
    # Save file temporarily
    file_type = file.filename.split(".")[-1].lower()
    file_contents = await file.read()
    
    # Extract text based on file type
    if file_type == "pdf":
        text = extract_text_from_pdf(file_contents)
    elif file_type == "txt":
        text = file_contents.decode("utf-8")
    else:
        raise ValueError("Unsupported file type")
    
    # Chunk the text
    if chunk_method == "semantic":
        chunks = semantic_chunking(text)
    else:
        raise ValueError("Unsupported chunking method")
    
    return {
        "original_text": text,
        "chunks": chunks,
        "file_name": file.filename,
        "file_type": file_type,
        "file_size": len(file_contents)
    }

def extract_text_from_pdf(pdf_contents: bytes) -> str:
    pdf_reader = PdfReader(io.BytesIO(pdf_contents))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.strip()