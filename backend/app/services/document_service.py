from app.db.supabase_client import get_supabase_client
from fastapi import HTTPException

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