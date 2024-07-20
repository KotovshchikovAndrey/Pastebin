from fastapi import FastAPI
from pydantic import ValidationError
import uvicorn
from adapters.transport.rest.exception_handlers import (
    handle_domain_exception,
    handle_internal_exception,
    handle_validation_exception,
)
from config import settings
from adapters.transport.rest import api_v1_router
from domain.exceptions.base import DomainException

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(ValidationError, handle_validation_exception)
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
