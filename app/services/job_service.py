from sqlalchemy.orm import Session
from app.models.job import Job
from app.repositories.job_repository import JobRepository



class JobService:

    @staticmethod
    def create_job_service(db:Session,job) -> Job:
        new_job = Job(
            job_name = job.job_name,
            description = job.description,
            job_type = job.job_type,
            payload = job.payload
        )

        return JobRepository.create(job=new_job,db=db)

    @staticmethod
    def get_job_service(job_id,db)->Job:
        return JobRepository.get_job(job_id=job_id,db=db)

    @staticmethod
    def fetch_all_jobs_service(db)->Job:
        return JobRepository.get_jobs(db=db)

    
