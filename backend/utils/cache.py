import redis.asyncio as redis
from redis.asyncio import Redis

from config import settings as global_settings


async def init_redis_pool() -> redis.Redis:
    redis_c = await redis.from_url(
        global_settings.redis_url,
        encoding="utf-8",
        db=global_settings.redis_db,
        decode_responses=True,
        password=global_settings.redis_password,
    )
    return redis_c


async def set_cache(redis_client: Redis, prefix: str, payload, expire: int) -> None:
    await redis_client.set(prefix, payload, ex=expire)


async def delete_cached_key(redis_client: Redis, key: str) -> None:
    await redis_client.delete(key)
