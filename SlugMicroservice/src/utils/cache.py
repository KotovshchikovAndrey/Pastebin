import asyncpg
from redis import Redis
from utils import base62


async def prepare_cache(database: asyncpg.Connection, cache: Redis) -> None:
    """Load all released slugs to redis cache"""

    query = """SELECT id FROM slug WHERE is_released = true;"""
    records = await database.fetch(query)

    released_slugs = dict()
    for record in records:
        slug_id, slug = record["id"], base62.encode_base62(record["id"])
        released_slugs[slug] = slug_id

    if released_slugs:
        await cache.zadd("released:slugs", mapping=released_slugs)
