from fastapi import APIRouter, File, UploadFile

from app.db.supabase_client import get_supabase_client
from app.models.schemas import UploadDocumentResponse
from app.services.storage_service import save_uploaded_file
from app.services.document_service import create_document_record
from app.services.job_service import create_job_record


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    supabase = get_supabase_client()

    document_details = await save_uploaded_file(file)
    result = await create_document_record(document_details)
    job_id = await create_job_record(result['id'])

    return {
        "document_id": result['id'],
        "job_id": job_id,
        "status": "pending",
    }