from redis import Redis

redis_client = Redis(
    port=6379,
    host="localhost",
    decode_responses = True,
    socket_timeout=None
)