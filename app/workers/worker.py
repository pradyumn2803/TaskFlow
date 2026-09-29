from app.redis import redis_client
from app.queue import QUEUE_NAME

def start_worker():
    print("worker stated....")

    while True:
        result = redis_client.brpop(QUEUE_NAME)

        if result is None:
            continue

        _, job_id = result

        print(f"executing job: {job_id}")


if __name__ == "__main__":
    start_worker()