from fastapi import FastAPI,Depends
from typing import Any
from pydantic import BaseModel, Field

from app.models.job import Job
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.job_service import JobService

from uuid import UUID
from fastapi import HTTPException

app = FastAPI()


class createJob(BaseModel):
    job_name: str = Field(min_length=1)
    description: str | None = None
    job_type: str=Field(min_length=1)
    payload: dict[str,Any]

@app.post("/jobs")
def create_jobs(job:createJob,db:Session = Depends(get_db)):
    new_job = JobService.create_job_service(
        job=job,
        db=db
    )

    return {
        "job_id": new_job.id,
        "job_name": new_job.job_name,
        "description": new_job.description,
        "job_type": new_job.job_type,
        "payload": new_job.payload,
        "status": new_job.status,
        "attempt_count": new_job.attempt_count,
        "created_at": new_job.created_at
    }

@app.get("/jobs/{job_id}")
def get_jobs(
    job_id:UUID,db:Session = Depends(get_db)
):
    job = JobService.get_job_service(job_id=job_id,db=db)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job Id not found"
        )

    return {
        "job_id": job.id,
        "job_name": job.job_name,
        "description": job.description,
        "job_type": job.job_type,
        "payload": job.payload,
        "status": job.status,
        "attempt_count": job.attempt_count,
        "created_at": job.created_at
    }

@app.get("/jobs")
def get_jobs(
    db:Session = Depends(get_db)
):
    jobs = JobService.fetch_all_jobs_service(db=db)

    return [{
        "job_id": job.id,
        "job_name": job.job_name,
        "description": job.description,
        "job_type": job.job_type,
        "payload": job.payload,
        "status": job.status,
        "attempt_count": job.attempt_count,
        "created_at": job.created_at
    } for job in jobs]
    