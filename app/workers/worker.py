from app.redis import redis_client
from app.queue import QUEUE_NAME
from app.database import SessionLocal
from uuid import UUID
from app.models.job import Job
from app.services.job_service import JobService


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

            print(f"executing job {job_id}")
            
        finally:
            db.close()

if __name__ == "__main__":
    start_worker()