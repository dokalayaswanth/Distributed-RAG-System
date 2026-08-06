from app.db.supabase_client import get_supabase_client


def save_chunks(document_id: str, chunks: list[dict]) -> list[dict]:
    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    if not chunks:
        raise ValueError("Chunks cannot be empty.")

    supabase = get_supabase_client()

    supabase.table("chunks").delete().eq("document_id", document_id).execute()

    rows = []

    for chunk in chunks:
        rows.append(
            {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "page_number": None,
                "vector_index_position": None,
            }
        )

    result = supabase.table("chunks").insert(rows).execute()

    if not result.data:
        raise ValueError("Failed to save chunks.")

    return result.data

def update_chunk_vector_index(saved_chunks: list[dict], vector_positions: list[int]) -> None:
    if not saved_chunks:
        raise ValueError("Saved chunks cannot be empty.")

    if not vector_positions:
        raise ValueError("Vector positions cannot be empty.")

    if len(saved_chunks) != len(vector_positions):
        raise ValueError("The number of saved chunks must match the number of vector positions.")

    supabase = get_supabase_client()

    for chunk, vector_index in zip(saved_chunks, vector_positions):
        result = supabase.table("chunks").update({"vector_index_position": vector_index}).eq("id", chunk["id"]).execute()
        if not result.data:
            raise ValueError(f"Failed to update vector position for chunk {chunk['id']}.")