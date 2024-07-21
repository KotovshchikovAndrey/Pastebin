import typing as tp

from pydantic import BaseModel, Field
from domain.config.enums import ExpirationEnum


class ResponseSchema(BaseModel):
    message: str
    data: tp.Annotated[dict | None, Field(default=None)]


class ErrorResponseSchema(BaseModel):
    message: str
    detail: tp.Annotated[list | None, Field(default=None)]


class ReadPasteSchema(BaseModel):
    password: tp.Annotated[str | None, Field(default=None)]


class CreatePasteSchema(BaseModel):
    text: str
    title: tp.Annotated[str | None, Field(default=None)]
    expiration: tp.Annotated[ExpirationEnum | None, Field(default=None)]
    category: tp.Annotated[str | None, Field(default=None)]
    password: tp.Annotated[str | None, Field(default=None)]
