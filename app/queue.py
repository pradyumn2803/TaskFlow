from app.redis import redis_client

QUEUE_NAME="taskflow:jobs"

def enqueue_job(job_id:str)->None:
    redis_client.lpush(QUEUE_NAME,job_id)

def dequeue_job()->None:
    redis_client.rpop(QUEUE_NAME)