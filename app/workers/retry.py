from datetime import timedelta,timezone,datetime
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DELAY_SECONDS = int(os.getenv("BASE_DELAY_SECONDS"))

def calculate_retry_time(
        attempt_count:int
)-> datetime:

    delay_seconds = BASE_DELAY_SECONDS * (2 ** (attempt_count - 1))
    print(BASE_DELAY_SECONDS, type(BASE_DELAY_SECONDS))
    print(attempt_count, type(attempt_count))

    return datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)