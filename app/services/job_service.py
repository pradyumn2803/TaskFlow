from sqlalchemy.orm import Session
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.queue import enqueue_job
from uuid import UUID


class JobService:

    @staticmethod
    def create_job_service(db:Session,job) -> Job:
        new_job = Job(
            job_name = job.job_name,
            description = job.description,
            job_type = job.job_type,
            payload = job.payload
        )

        new_job= JobRepository.create(job=new_job,db=db)

        enqueue_job(str(new_job.id))

        return new_job

    @staticmethod
    def get_job_service(job_id,db)->Job:
        return JobRepository.get_job(job_id=job_id,db=db)

    @staticmethod
    def fetch_all_jobs_service(db)->Job:
        return JobRepository.get_jobs(db=db)

    @staticmethod
    def claim_job(job_id:UUID,db:Session)->bool:
        return JobRepository.claim_job(job_id=job_id,db=db)

    @staticmethod
    def mark_success(job_id:UUID,db:Session)->None:
        JobRepository.mark_success(job_id=job_id,db=db)

    @staticmethod
    def mark_fail(job_id:UUID,error:str,db:Session)->None:
        JobRepository.mark_fail(job_id=job_id,error=error,db=db)

    @staticmethod
    def retry_job(job_id:UUID,db:Session)->None:
        JobRepository.retry_job(job_id=job_id,db=db)
