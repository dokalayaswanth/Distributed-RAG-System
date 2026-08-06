from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import retrieve_chunks
from app.services.log_service import query_log


router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.post("/", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query should not be empty.",
        )

    if request.k <= 0:
        raise HTTPException(
            status_code=400,
            detail="k must be greater than 0.",
        )

    if request.mode == "rag":
        raise HTTPException(
            status_code=501,
            detail="RAG mode is not implemented yet.",
        )

    if request.mode != "retrieval":
        raise HTTPException(
            status_code=400,
            detail="Only retrieval mode is supported for now.",
        )

    try:
        sources = retrieve_chunks(
            query=request.query,
            k=request.k,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    log_data = {
        "query": request.query,
        "top_k": request.k,
        "mode": request.mode,
        "answer": "retrieval_only",
    }
    query_log(log_data)
    return {
        "answer": None,
        "sources": sources,
        "mode": "retrieval",
    }