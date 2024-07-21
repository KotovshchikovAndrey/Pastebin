import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from adapters.storage.memcached.connection import MemcachedConnection
from adapters.storage.sql.connection import SqlDatabaseConnection
from adapters.transport.grpc.client import GrpcAsyncClient
from adapters.transport.rest import api_v1_router
from adapters.transport.rest.exception_handlers import (
    handle_domain_exception,
    handle_internal_exception,
    handle_validation_exception,
)
from config import settings
from config.ioc import container
from domain.exceptions.base import DomainException


async def shutdown():
    database = container.get(SqlDatabaseConnection)
    memcached = container.get(MemcachedConnection)
    grpc = container.get(GrpcAsyncClient)

    await asyncio.gather(
        database.close(),
        memcached.close(),
        grpc.close(),
    )

    print("Close")


app = FastAPI(on_shutdown=[shutdown])
app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(RequestValidationError, handle_validation_exception)
app.add_exception_handler(DomainException, handle_domain_exception)
app.add_exception_handler(Exception, handle_internal_exception)


def run_uvicorn_server() -> None:
    uvicorn.run(
        "index:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.worker_count,
        reload=settings.server.is_debug,
    )
