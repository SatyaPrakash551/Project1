import redis.asyncio as redis
from dotenv import load_dotenv
import os
load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)
