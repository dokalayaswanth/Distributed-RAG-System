from app.db.supabase_client import get_supabase_client
from fastapi import HTTPException
from datetime import datetime, timezone

async def create_document_record(document_details):
    supabase = get_supabase_client()
    document_insert = supabase.table("documents").insert({
        "id": document_details['id'],
        "file_name": document_details['file_name'],
        "file_type": document_details['file_type'],
        "file_size": document_details['file_size'],
        "storage_path": document_details['storage_path']
    }).execute()

    if not document_insert.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create document record.",
        )

    return document_insert.data[0]

def get_document_details(document_id: str | None = None) -> dict:
    if not document_id:
        raise ValueError("Document Id is required.")
    supabase = get_supabase_client()

    document_details = supabase.table("documents").select("id, file_name, file_type, file_size, storage_path").eq("id", document_id).execute()

    if not document_details.data:
        raise ValueError(f"Document with id {document_id} is not found.")
    return document_details.data[0]


def mark_document_processing(document_id: str):
    supabase = get_supabase_client()

    if not document_id:
        raise ValueError("Document Id should not be empty.")
    
    result = supabase.table("documents").update({
        "status": "processing",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", document_id).execute()

    if not result.data:
        raise ValueError(f"Document with id {document_id} was not found.")
    return result.data[0]

def mark_document_indexed(document_id: str):
    supabase = get_supabase_client()

    if not document_id:
        raise ValueError("Document Id should not be empty.")
    
    result = supabase.table("documents").update({
        "status": "indexed",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", document_id).execute()

    if not result.data:
        raise ValueError(f"Document with id {document_id} was not found.")
    return result.data[0]