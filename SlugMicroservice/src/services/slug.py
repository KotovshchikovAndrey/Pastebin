import typing as tp

import asyncpg
import utils.base62 as base62
from redis import Redis


Slug = tp.NewType("Slug", str)


class SlugService:
    _database: asyncpg.Connection
    _cache: Redis

    def __init__(self, database: asyncpg.Connection, cache: Redis) -> None:
        self._database = database
        self._cache = cache

    async def get_unique_slug(self) -> Slug:
        result = await self._cache.zpopmin("released:slugs")
        if result:
            slug, slug_id = result[0]
            query = """UPDATE slug SET is_released = $1 WHERE id = $2;"""
            await self._database.execute(query, False, slug_id)
            return slug.decode()

        query = """INSERT INTO slug VALUES (DEFAULT, DEFAULT) RETURNING id;"""
        slug_id: int = await self._database.fetchval(query)
        return base62.encode_base62(slug_id)

    async def release_slug(self, slug: str) -> None:
        slug_id = base62.decode_base62(slug)
        query = """UPDATE slug SET is_released = $1 WHERE id = $2;"""
        await self._database.execute(query, True, slug_id)
        await self._cache.zadd("released:slugs", mapping={slug: slug_id})
