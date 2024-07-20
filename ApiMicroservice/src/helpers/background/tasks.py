import asyncio
from celery import shared_task
from injector import NoScope

from adapters.transport.grpc.client import GrpcAsyncClient
from adapters.transport.grpc.providers.slug import SlugGrpcProvider
from config import settings
from config.ioc import container
from adapters.storage.memcached.cache import InMemoryCacheSystem
from adapters.storage.memcached.connection import MemcachedConnection
from adapters.storage.sql.connection import SqlDatabaseConnection
from adapters.storage.sql.repositories.paste import PasteSqlRepository
from domain.ports.cache import CachedValue


async def cache_popular_pastes_async():
    sql_database = container.get(SqlDatabaseConnection, scope=NoScope)
    cache_database = container.get(MemcachedConnection, scope=NoScope)

    repository = PasteSqlRepository(sql_database)
    cache = InMemoryCacheSystem(cache_database, ttl=settings.cache.ttl)

    popular_pastes = await repository.get_popular()
    await repository.reset_views()

    cached_values = [
        CachedValue(key=paste.slug, data=paste.model_dump_json())
        for paste in popular_pastes
    ]

    await cache.add_many(cached_values)
    await asyncio.gather(*[sql_database.close(), cache_database.close()])


async def delete_expired_pastes_async():
    sql_database = container.get(SqlDatabaseConnection, scope=NoScope)
    repository = PasteSqlRepository(sql_database)

    grpc = container.get(GrpcAsyncClient, scope=NoScope)
    slug_provider = SlugGrpcProvider(grpc.channel)
    released_slugs = await repository.delete_expired()

    async with asyncio.TaskGroup() as tg:
        for slug in released_slugs:
            tg.create_task(slug_provider.release_slug(slug))

    await sql_database.close()
    await grpc.close()


@shared_task
def cache_popular_pastes():
    asyncio.run(cache_popular_pastes_async())


@shared_task
def delete_expired_pastes():
    asyncio.run(delete_expired_pastes_async())
