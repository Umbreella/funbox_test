import redis

from app.settings import settings

redis_cli = redis.Redis(**{
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
})


async def get_redis():
    return redis_cli
