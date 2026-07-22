from fastapi import APIRouter, HTTPException
from app.services.job_service import get_job_record
from app.models.schemas import JobByIdResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/{job_id}", response_model=JobByIdResponse)
async def get_job_details(job_id):
    job = get_job_record(job_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    return job