from aiomcache import Client


class MemcachedConnection:
    _client: Client

    def __init__(self, host: str, port: int, pool_size: int = 1) -> None:
        self._client = Client(host=host, port=port, pool_size=pool_size)

    def get_client(self) -> Client:
        return self._client

    async def close(self) -> None:
        await self._client.close()
