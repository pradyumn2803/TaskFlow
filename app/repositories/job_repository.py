from sqlalchemy.orm import Session
from app.models.job import Job
from sqlalchemy import select

class JobRepository:

    @staticmethod
    def create(
        db: Session,
        job: Job
    ) -> Job:
        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def get_job(job_id,db)-> Job| None:
        return db.get(Job,job_id)

    @staticmethod
    def get_jobs(db)-> list[Job]:
        statement = select(Job).order_by(Job.created_at.desc())

        return list(db.scalars(statement).all())

