from sqlalchemy.orm import Session
from app.models.job import Job
from sqlalchemy import select,update

from app.models.job import Job,JobStatus
from uuid import UUID
from datetime import datetime,timezone

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

    @staticmethod
    def claim_job(
        db:Session,
        job_id:UUID
    )->bool:
        
        statement = (update(Job).where(
            Job.id == job_id,
            Job.status == JobStatus.PENDING
        ).values(
            status = JobStatus.RUNNING,
            started_at = datetime.now(timezone.utc)
        ))

        result = db.execute(statement)
        db.commit()

        return result.rowcount == 1
