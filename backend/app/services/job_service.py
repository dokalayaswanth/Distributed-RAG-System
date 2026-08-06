from app.db.supabase_client import get_supabase_client
from uuid import uuid4
from fastapi import HTTPException
from app.models.schemas import JobByIdResponse, pending_job
from datetime import datetime, timezone

async def create_job_record(document_id):
    supabase = get_supabase_client()

    if document_id is None:
        raise HTTPException(status_code=400, detail="Document ID is required to create a job record.")
    job_id = f"{uuid4()}"
    
    result = supabase.table('ingestion_jobs').insert({
        "id": job_id,
        "document_id": document_id,
        "status": "pending"
    }).execute()

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create ingestion job.",
        )
    return job_id

def get_job_record(job_id: str) -> JobByIdResponse | None:
    supabase = get_supabase_client()
    
    result = supabase.table('ingestion_jobs').select('id, document_id, status, error_message').eq(
        "id", job_id
    ).execute()
    if not result.data:
        return None
    job = result.data[0]
    return JobByIdResponse(
        document_id=job['document_id'],
        job_id=job['id'],
        status=job['status'],
        error_message = job['error_message']
    )

def get_pending_jobs() -> pending_job | None:
    supabase = get_supabase_client()

    pending_jobs = supabase.table('ingestion_jobs').select('id, document_id, status, created_at').eq(
        "status", "pending"
    ).limit(1).order("created_at").execute()

    if not pending_jobs.data:
        return None

    return pending_jobs.data[0]

def mark_job_processing(job_id: str):
    supabase = get_supabase_client()

    if not job_id:
        raise ValueError("Job Id should not be empty.")
    
    result = supabase.table("ingestion_jobs").update({
        "status": "processing",
        "started_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", job_id).execute()

    if not result.data:
        raise ValueError(f"Job with id {job_id} was not found.")

    return result.data[0]

def mark_job_completed(job_id: str):
    if not job_id:
        raise ValueError("Job Id should not be empty.")
    supabase = get_supabase_client()
    result = supabase.table('ingestion_jobs').update({
        "status": "completed",
        "completed_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", job_id).execute()

    if not result.data:
        raise ValueError(f"Job with id {job_id} was not found.")

    return result.data[0]