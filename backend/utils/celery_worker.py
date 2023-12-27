import asyncio
import functools

from celery import Celery

from utils.cache import init_redis_pool
from config import settings

celery = Celery(
    "tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


@celery.task()
@sync
async def celery_set_cache(cache_key: str, payload: str, expire: int):
    redis_client = await init_redis_pool()
    await redis_client.set(cache_key, payload, ex=expire)


@celery.task()
@sync
async def celery_delete_cached_key(
    cache_key: str,
):
    redis_client = await init_redis_pool()
    await redis_client.delete(cache_key)
