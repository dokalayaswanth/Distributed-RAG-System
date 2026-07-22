from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException

from app.config import settings
from app.models.schemas import StorageServiceResponse

async def save_uploaded_file(file: UploadFile) -> StorageServiceResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required.")
    file_name = file.filename
    file_extension = Path(file_name).suffix.lower()

    if file_extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_extension}' is not allowed. Allowed types: {settings.allowed_extensions}",
        )

    if file.content_type not in settings.allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail=f"Content type '{file.content_type}' is not allowed. Allowed types: {settings.allowed_content_types}",
        )
    
    file_bytes = await file.read()
    file_size = len(file_bytes)

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if file_size > settings.max_upload_size_bytes:
        raise HTTPException(
            status=400,
            detail="FIle size exceeds the limit"
        )
    
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    unique_file_name = f"{uuid4()}{file_extension}"
    file_path = upload_dir / unique_file_name

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return {
        "id": unique_file_name.split('.')[0],
        "document_id": unique_file_name,
        "file_name": file_name,
        "file_type": file_extension.replace(".", ""),
        "file_size": file_size,
        "storage_path": str(file_path.as_posix()),
    }