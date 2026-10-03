from app.redis import redis_client
from app.queue import QUEUE_NAME,enqueue_job
from app.database import SessionLocal
from uuid import UUID
from app.models.job import Job
from app.services.job_service import JobService
from app.workers.handlers.dispatcher import execute_job
from app.workers.exceptions import RetryableJobError,PermanentJobError
from app.workers.retry import calculate_retry_time
from dotenv import load_dotenv
import time
import os

load_dotenv()

max_retries = int(os.getenv("MAX_RETRIES"))

def start_worker():
    print("worker stated....")

    while True:
        result = redis_client.brpop(QUEUE_NAME)

        if result is None:
            continue

        _, job_id = result
        print("Redis result:", job_id)

        db=SessionLocal()
        job_id=UUID(job_id)
        try:
            claimed = JobService.claim_job(job_id=job_id,db=db)

            if claimed is None:
                print(f"job already claimed: {job_id}")
                continue
            job = db.get(Job,job_id)

            if not job:
                raise ValueError(f"job not found for this id:{job_id}")

            print(f"executing job {job_id}")

            try:
                # time.sleep(5)
                execute_job(
                    job.job_type,
                    job.payload
                )

                JobService.mark_success(
                    job_id=job_id,
                    db=db
                )

                print(f"Job {job_id} completed successfully")

            except RetryableJobError as e:
                print(f"Job {job_id} failed Temporalily: {e}")

                next_retry_at = calculate_retry_time(attempt_count=job.attempt_count)
                print(f"next_retry_at::::: {next_retry_at}")
                
                if max_retries >= job.attempt_count:
                    JobService.retry_job(job_id=job_id,db=db,next_retry_at=next_retry_at)

                    print(f"{job_id} returned to queue for execution....")

                else:
                    JobService.mark_fail(job_id=job_id,error=str(e),db=db)

                    print(f"Maximum attempts reached :{job_id} permanently failed after {job.attempt_count} attempts")

            except Exception as e:
                JobService.mark_fail(
                    job_id=job_id,
                    error=str(e),
                    db=db
                )
                print(f"Job {job_id} failed: {e}")
            
        finally:
            db.close()

if __name__ == "__main__":
    start_worker()