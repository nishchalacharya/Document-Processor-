from supabase import create_client
from config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

# We'll use Supabase's pgvector extension for embeddings
# Make sure to enable the pgvector extension in your Supabase database

# Table creation SQL (run this once in Supabase SQL editor):
"""
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    upload_time TIMESTAMP DEFAULT NOW(),
    chunking_method TEXT NOT NULL,
    embedding_model TEXT NOT NULL
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id),
    chunk_text TEXT NOT NULL,
    chunk_number INTEGER NOT NULL,
    embedding vector(384)  -- Adjust based on your embedding model
);
"""


# response=supabase.table("document_chunks").select("chunk_text").execute()

# data=response.data

# for x in data:
#     print(x)