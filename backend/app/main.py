from fastapi import FastAPI
from app.routers import health_router, documents_router, jobs_router

app = FastAPI(
    title="Distributed RAG System",
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(jobs_router)