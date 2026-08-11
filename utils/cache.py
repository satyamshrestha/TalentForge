import logging

from redis.exceptions import RedisError

from db.redis import redis_client

logger = logging.getLogger("talentforge.cache")


def cache_get(key: str):
    try:
        return redis_client.get(key)
    except RedisError:
        logger.exception(
            "Redis cache get failed | key=%s",
            key,
        )
        return None


def cache_set(
    key: str,
    value: str,
    ttl: int,
):
    try:
        redis_client.set(
            key,
            value,
            ex=ttl,
        )
    except RedisError:
        logger.exception(
            "Redis cache set failed | key=%s",
            key,
        )


def cache_delete(key: str):
    try:
        redis_client.delete(key)
    except RedisError:
        logger.exception(
            "Redis cache delete failed | key=%s",
            key,
        )