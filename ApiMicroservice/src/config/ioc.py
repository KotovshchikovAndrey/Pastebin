import injector

from adapters.storage.memcached.cache import InMemoryCacheSystem
from adapters.storage.memcached.connection import MemcachedConnection
from adapters.storage.sql.connection import SqlDatabaseConnection
from adapters.storage.sql.repositories.paste import PasteSqlRepository
from adapters.transport.grpc.client import GrpcAsyncClient
from adapters.transport.grpc.providers.slug import SlugGrpcProvider
from config import settings

from domain.ports.cache import ICacheSystem
from domain.ports.paste import IPasteRepository
from domain.ports.slug import ISlugProvider
from domain.services.paste import PasteService


class AdaptersProvider(injector.Module):
    @injector.singleton
    @injector.provider
    def provide_memcache_database(self) -> MemcachedConnection:
        return MemcachedConnection(
            host=settings.cache.memcached_host,
            port=settings.cache.memcached_port,
        )

    @injector.singleton
    @injector.provider
    def provide_sql_database(self) -> SqlDatabaseConnection:
        return SqlDatabaseConnection(
            url=settings.database.postgres_url,
            echo=settings.database.echo,
        )

    @injector.singleton
    @injector.provider
    def provide_paste_repository(
        self, database: SqlDatabaseConnection
    ) -> IPasteRepository:
        return PasteSqlRepository(database)

    @injector.singleton
    @injector.provider
    def provide_cache_system(self, database: MemcachedConnection) -> ICacheSystem:
        return InMemoryCacheSystem(database, ttl=settings.cache.ttl)

    @injector.singleton
    @injector.provider
    def provide_grpc_client(self) -> GrpcAsyncClient:
        return GrpcAsyncClient(grpc_channel_address=settings.provider.slug_address)

    @injector.singleton
    @injector.provider
    def provide_slug_provider(self, client: GrpcAsyncClient) -> ISlugProvider:
        return SlugGrpcProvider(channel=client.channel)


class DomainProvider(injector.Module):
    @injector.singleton
    @injector.provider
    def provide_paste_service(
        self,
        repository: IPasteRepository,
        cache: ICacheSystem,
        slug: ISlugProvider,
    ) -> PasteService:
        return PasteService(repository=repository, cache=cache, slug=slug)


container = injector.Injector([AdaptersProvider, DomainProvider])
