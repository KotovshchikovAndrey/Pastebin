from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from adapters.transport.rest.schemas import ErrorResponseSchema
from domain.exceptions.base import DomainException
from domain.exceptions.paste import (
    CategoryNotFoundException,
    InvalidPasswordException,
    PasteNotFoundException,
)


def handle_validation_exception(request: Request, exc: ValidationError):
    response = ErrorResponseSchema(message="Invalid request", detail=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump(),
    )


def handle_internal_exception(request: Request, exc: Exception):
    response = ErrorResponseSchema(message="Internal server error")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(),
    )


def handle_domain_exception(request: Request, exc: DomainException):
    response = ErrorResponseSchema(message=exc.message)

    if any(
        [
            isinstance(exc, PasteNotFoundException),
            isinstance(exc, CategoryNotFoundException),
        ]
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump(),
        )

    if isinstance(exc, InvalidPasswordException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=response.model_dump(),
        )
