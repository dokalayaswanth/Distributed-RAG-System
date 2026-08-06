# Distributed RAG-Based AI Inference and Document Retrieval System

A distributed-style AI document retrieval system that allows users to upload PDF/TXT documents, process them asynchronously, create vector embeddings, store searchable chunks, and ask natural language questions using Retrieval-Augmented Generation (RAG).

## Project Overview

This project is designed to go beyond a basic single-service RAG application. It separates real-time API requests from long-running document processing tasks using an API service and a background worker service.

Users can upload documents, track ingestion job status, and query indexed documents. The system retrieves relevant chunks using FAISS semantic search and generates source-grounded answers using an LLM.

## Key Features

- Upload PDF and TXT documents
- Asynchronous document ingestion using background workers
- Job status tracking for uploaded documents
- Text parsing and chunking
- Embedding generation using sentence-transformers
- Vector similarity search using FAISS
- Retrieval-only mode for debugging
- RAG mode for LLM-powered answers
- Source-grounded responses with document references
- Supabase/PostgreSQL metadata storage
- Index version tracking
- Docker-based service separation

## Architecture

```text
Client / Frontend
   |
   v
API Service
   |-- document upload
   |-- job creation
   |-- job status
   |-- query endpoint
   |
   v
Shared Database / Storage
   |-- documents
   |-- ingestion jobs
   |-- chunks
   |-- index versions
   |-- query logs
   |
   v
Worker Service
   |-- parses documents
   |-- chunks text
   |-- generates embeddings
   |-- updates FAISS index
   |-- updates job status
   |
   v
RAG Query Flow
   |-- embed query
   |-- search FAISS
   |-- retrieve top-k chunks
   |-- call LLM
   |-- return answer with sources
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Uvicorn, Pydantic |
| Worker | Python background process |
| Database | Supabase / PostgreSQL |
| Vector Search | FAISS |
| Embeddings | sentence-transformers |
| Document Parsing | pypdf, plain text parser |
| LLM | Groq / OpenAI-compatible provider |
| Deployment | Docker, Docker Compose |

## Planned Folder Structure

```text
distributed-rag-system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── db/
│   │   └── utils/
│   ├── worker/
│   │   ├── worker.py
│   │   └── ingestion_worker.py
│   ├── data/
│   │   ├── uploads/
│   │   └── faiss_index/
│   ├── requirements.txt
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   └── .env.example
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Core API Endpoints

### Health Check

```http
GET /health
```

Returns API health and index status.

### Upload Document

```http
POST /documents/upload
```

Uploads a PDF/TXT document, creates a document record, and creates a pending ingestion job.

### Get Job Status

```http
GET /jobs/{job_id}
```

Returns the current status of a document ingestion job.

### Query Documents

```http
POST /query
```

Supports both retrieval-only mode and RAG answer mode.

Example request:

```json
{
  "query": "What is this document about?",
  "k": 4,
  "mode": "rag"
}
```

Example response:

```json
{
  "answer": "The document explains...",
  "sources": [
    {
      "document_id": "doc_123",
      "chunk_id": "chunk_5",
      "score": 0.84,
      "preview": "Relevant document content..."
    }
  ]
}
```

## Environment Variables

Create a `.env` file based on `.env.example`.

```env
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

LLM_API_KEY=
LLM_MODEL=

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

FAISS_INDEX_PATH=data/faiss_index/index.faiss
FAISS_METADATA_PATH=data/faiss_index/metadata.json

UPLOAD_DIR=data/uploads
TOP_K_DEFAULT=4
```

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd distributed-rag-system
```

### 2. Create a virtual environment

```bash
cd backend
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then fill in your Supabase and LLM provider credentials.

### 5. Run the API service

```bash
uvicorn app.main:app --reload
```

### 6. Run the worker service

In a separate terminal:

```bash
python worker/worker.py
```

## Docker Setup

Once Docker support is added, run:

```bash
docker compose up --build
```

This should start the API service and worker service separately.

## Database Tables

The system is designed around these main tables:

- `documents`
- `ingestion_jobs`
- `chunks`
- `index_versions`
- `query_logs`

These tables store uploaded document metadata, processing status, chunk references, vector index versions, and query history.

## Development Roadmap

- [ ] Create FastAPI backend foundation
- [ ] Add health endpoint
- [ ] Add Supabase/PostgreSQL schema
- [ ] Add document upload endpoint
- [ ] Add ingestion job creation
- [ ] Add job status endpoint
- [ ] Implement document parser
- [ ] Implement chunking service
- [ ] Implement embedding service
- [ ] Implement FAISS vector store
- [ ] Create background worker process
- [ ] Add retrieval-only query mode
- [ ] Add RAG answer generation
- [ ] Add index versioning
- [ ] Add query logging
- [ ] Add Docker Compose
- [ ] Add frontend, optional
- [ ] Prepare cloud deployment

## Why This Project Matters

This project demonstrates practical AI engineering and backend system design. It combines document processing, asynchronous workers, vector search, LLM integration, API development, and distributed-style architecture.

It is useful for learning and showcasing skills in:

- AI/ML application development
- RAG pipelines
- FastAPI backend development
- Background processing
- Vector databases and semantic search
- Cloud-ready system design
- Distributed system fundamentals