import asyncio
from concurrent import futures
import signal
import asyncpg
import grpc

from redis import asyncio as aioredis
from api.grpc import SlugGrpcController
from proto.py import slug_service_pb2_grpc
from services.slug import SlugService
from settings import AppSettings


async def run_server():
    settings = AppSettings()

    cache = aioredis.from_url(settings.cache.redis_url)
    database: asyncpg.Connection = await asyncpg.connect(
        user=settings.database.postgres_username,
        password=settings.database.postgres_password,
        database=settings.database.postgres_db,
        host=settings.database.postgres_host,
        port=settings.database.postgres_port,
    )

    slug_service = SlugService(database=database, cache=cache)
    slug_controller = SlugGrpcController(service=slug_service)

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=1))
    slug_service_pb2_grpc.add_SlugServiceServicer_to_server(slug_controller, server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()

    shutdown = asyncio.Event()

    def on_shutdown(*args, **kwargs):
        print("Shutdown!")
        shutdown.set()

    signal.signal(signal.SIGINT, on_shutdown)
    await shutdown.wait()

    await asyncio.gather(
        cache.aclose(),
        database.close(),
        server.stop(10),
    )

    print("Server close!")


if __name__ == "__main__":
    asyncio.run(run_server())
