from app.services.document_service import get_document_details, mark_document_processing, mark_document_indexed
from app.services.job_service import get_pending_jobs, mark_job_processing, mark_job_completed
from app.services.document_parser import parse_document
from app.services.chunker import chunk_text
from app.services.chunk_service import save_chunks, update_chunk_vector_index
from app.services.embedder import embed_texts
from app.services.vector_store import add_vectors

def run_ingestion_worker_once() -> None:
    print("Worker started")
    print("Checking for pending ingestion jobs...")

    job = get_pending_jobs()

    if not job:
        print("No pending jobs found")
        return

    job_id = job["id"]
    document_id = job["document_id"]

    print(f"Picked job_id: {job_id}")
    print(f"Related document_id: {document_id}")

    updated_job = mark_job_processing(job_id)

    document = get_document_details(document_id)

    updated_document = mark_document_processing(document_id)

    print("Job marked as processing:")
    print(updated_job)

    print("Document details:")
    print(document)

    print("Document marked as processing:")
    print(updated_document)

    print(f"Started parsing the document {document['id']}")
    parsed_text = parse_document(document["storage_path"])
    print(f"Parsed text length: {len(parsed_text)}")

    print(f"Started chunking the parsed text from the document {document['id']}")
    chunks = chunk_text(parsed_text)
    print(f"Chunk count: {len(chunks)}")
    # print("Preview of the chunks", chunks[0])

    print("Started saving the chunks.")
    saved_chunks = save_chunks(document["id"], chunks)
    print(f"Saved chunks: {len(saved_chunks)}")

    chunk_contents = [
        chunk["content"]
            for chunk in saved_chunks
            if chunk.get("content") and chunk["content"].strip()
    ]

    if not chunk_contents:
        raise ValueError("No valid chunk content found for embedding generation.")

    embeddings = embed_texts(chunk_contents)

    print(f"Generated embeddings for {len(embeddings)} chunks")
    print(f"Embedding shape: ({len(embeddings)}, {len(embeddings[0])})")

    faiss_metadata = []

    for chunk in saved_chunks:
        faiss_metadata.append(
            {
                "chunk_id": chunk["id"],
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "page_number": chunk.get("page_number"),
                "content": chunk["content"],
                "preview": chunk["content"][:200],
            }
        )

    faiss_result = add_vectors(
        vectors=embeddings,
        metadata=faiss_metadata,
    )

    print("FAISS update result:")
    print(faiss_result)

    update_chunk_vector_index(
        saved_chunks=saved_chunks,
        vector_positions=faiss_result["vector_positions"],
    )

    print(f"Updated chunks with vector_index_position")

    completed_job = mark_job_completed(job_id)
    print(f"Job marked as completed: {completed_job}")

    indexed_document = mark_document_indexed(document_id)
    print(f"Document marked as indexed: {indexed_document}")


    print("Worker finished one cycle")