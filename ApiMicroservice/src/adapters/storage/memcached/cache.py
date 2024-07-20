import asyncio
from aiomcache import Client
from adapters.storage.memcached.connection import MemcachedConnection
from domain.ports.cache import CachedValue, ICacheSystem


class InMemoryCacheSystem(ICacheSystem):
    _client: Client
    _ttl: int

    def __init__(self, database: MemcachedConnection, ttl: int) -> None:
        self._client = database.get_client()
        self._ttl = ttl

    async def get(self, key: str) -> str | None:
        data = await self._client.get(key.encode())
        if data is not None:
            return data.decode()

    async def add(self, cached_value: CachedValue) -> None:
        await self._client.add(
            key=cached_value.key.encode(),
            value=cached_value.data.encode(),
            exptime=self._ttl,
        )

    async def add_many(self, cached_values: list[CachedValue]) -> None:
        adds = [self.add(cached_value) for cached_value in cached_values]
        await asyncio.gather(*adds)

    async def delete(self, key: str) -> None:
        await self._client.delete(key.encode())

    async def clear(self) -> None:
        await self._client.flush_all()
