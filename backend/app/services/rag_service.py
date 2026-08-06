from app.services.embedder import embed_text
from app.services.vector_store import search_vectors

def retrieve_chunks(query: str, k: int)-> list[dict]:
    if not query:
        raise ValueError("Query should not be empty.")
    if k <= 0:
        raise ValueError("k should be a greater tha 0.")
    embeded_query = embed_text(query.strip())

    search_results = search_vectors(embeded_query, top_k=k)

    sources = []

    for result in search_results:
        metadata = result.get("metadata")

        if not metadata:
            continue

        content = metadata.get("content", "")

        preview = content[:300]

        sources.append(
            {
                "document_id": metadata.get("document_id", ""),
                "chunk_id": metadata.get("chunk_id", ""),
                "chunk_index": metadata.get("chunk_index", -1),
                "score": result.get("score", 0.0),
                "preview": preview,
            }
        )

    return sources