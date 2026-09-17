from fastapi import FastAPI
from typing import Any
from pydantic import BaseModel, Field

app = FastAPI()


class createJob(BaseModel):
    job_name: str = Field(min_length=1)
    description: str | None = None
    job_type: str=Field(min_length=1)
    payload: dict[str,Any]

@app.post("/jobs")
def create_jobs(job:createJob):
    return {
        "job_name": job.job_name,
        "description": job.description,
        "job_type": job.job_type,
        "payload": job.payload
    }