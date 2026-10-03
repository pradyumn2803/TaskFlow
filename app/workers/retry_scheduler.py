from app.database import SessionLocal
from app.services.job_service import JobService
from app.queue import enqueue_job
import time

def start_retry_scheduler():

    print("Retry Scheduler Started...")

    while True:

        db=SessionLocal()

        try:
            jobs = JobService.get_due_retry_jobs(db=db)

            for job in jobs:

                claimed = JobService.claim_due_retry_jobs(job_id=job.id,db=db)

                if not claimed:
                    continue

                enqueue_job(str(job.id))

                print(f"jobs enqueue id:{job.id}")

        finally:
            db.close()

        time.sleep(1)


if __name__ == "__main__":
    start_retry_scheduler()