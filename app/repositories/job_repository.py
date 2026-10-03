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
            Job.status == JobStatus.QUEUED
        ).values(
            status = JobStatus.RUNNING,
            started_at = datetime.now(timezone.utc),
            attempt_count = Job.attempt_count+1
        ))

        result = db.execute(statement)
        db.commit()

        return result.rowcount == 1

    @staticmethod
    def mark_success(
        job_id:UUID,
        db:Session
    )->None:
        statement = (
            update(Job).where(
                Job.id == job_id
            ).values(
                status = JobStatus.SUCCESS,
                completed_at = datetime.now(timezone.utc),
            )
        )

        db.execute(statement)
        db.commit()

    @staticmethod
    def mark_fail(
        job_id:UUID,
        db:Session,
        error:str
    )->None:
        statement = (
            update(Job).where(
                Job.id == job_id
            ).values(
                status = JobStatus.FAILED,
                completed_at = datetime.now(timezone.utc),
                error = error
            )
        )

        db.execute(statement)
        db.commit()

    @staticmethod
    def retry_job(
        job_id:UUID,
        db:Session,
        next_retry_at:datetime
    )->None:

        statement = update(Job).where(
            Job.id == job_id,
            Job.status == JobStatus.RUNNING
        ).values(
            status = JobStatus.PENDING,
            started_at = None,
            error = None,
            next_retry_at = next_retry_at
        )

        db.execute(statement)
        db.commit()


    @staticmethod
    def get_due_retry_jobs(
        db:Session
    )->list[Job] :

        statement = select(Job).where(
            Job.status == JobStatus.PENDING,
            Job.next_retry_at.is_not(None),
            Job.next_retry_at <= datetime.now(timezone.utc)
        ).order_by(Job.next_retry_at.asc())

        return list(db.scalars(statement).all())

    @staticmethod
    def claim_retry_due_job(
        db:Session,
        job_id:UUID
    )->bool:
        
        statement = (
            update(Job).where(
            Job.id == job_id,
            Job.status == JobStatus.PENDING,
            Job.next_retry_at.is_not(None),
            Job.next_retry_at <= datetime.now(timezone.utc)
        ).values(
            status = JobStatus.QUEUED,
            next_retry_at = None
        ))

        result = db.execute(statement)
        db.commit()

        return result.rowcount == 1
    
