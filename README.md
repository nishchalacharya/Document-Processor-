# Document Processing API with Semantic Search

A FastAPI-based service for processing PDFs/text documents, generating embeddings, and enabling semantic search using Supabase and pgvector.

## ✨ Key Features

- **Document Processing**: Upload and chunk PDFs/text files with semantic splitting
- **Vector Search**: Find relevant document sections using embedding similarity
- **Supabase Integration**: Store documents + embeddings with pgvector for efficient search
- **REST API**: Well-structured endpoints with Swagger UI documentation

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Embeddings**: [sentence-transformers]


## 🚀 Quick Start

1. **Setup environment**:
   ```bash
   git clone https://github.com/nishchalacharya/Document-Processor-.git
   cd Document-Processor
   pip install -r requirements.txt

2.Configure environment variables
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
EMBEDDING_MODEL=your-model-name

3.Run API:
   uvicorn main:app --reload
