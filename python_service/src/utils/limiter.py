from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["3 per minute", "1 per second"],
    storage_uri="redis://redis/0"
    )