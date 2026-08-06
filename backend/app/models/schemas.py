from pydantic import BaseModel
from datetime import datetime


class UploadDocumentResponse(BaseModel):
    document_id: str
    job_id: str
    status: str

class StorageServiceResponse(BaseModel):
    id: str
    document_id: str
    file_name: str
    file_type: str
    file_size: int
    storage_path: str

class JobByIdResponse(BaseModel):
    document_id: str
    job_id: str
    status: str
    error_message: str | None

class pending_job(BaseModel):
    job_id: str
    document_id: str
    status: str
    created_at: datetime