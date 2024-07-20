from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from domain.exceptions.base import DomainException
from domain.exceptions.paste import InvalidPasswordException, PasteNotFoundException


def handle_validation_exception(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "message": "Invalid request!",
                "detail": exc.errors(),
            }
        ),
    )


def handle_internal_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Внутренняя ошибка сервера!",
            "detail": None,
        },
    )


def handle_domain_exception(request: Request, exc: DomainException):
    response_data = {
        "message": exc.message,
        "detail": None,
    }

    if isinstance(exc, PasteNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_data,
        )

    if isinstance(exc, InvalidPasswordException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=response_data,
        )
