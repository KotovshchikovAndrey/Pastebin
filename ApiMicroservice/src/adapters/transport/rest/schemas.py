import typing as tp
import annotated_types as at
from pydantic import BaseModel, Field

from domain.config.enums import ExpirationEnum
from domain.dto.paste import CreatePasteDto


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        frozen = True


class PasswordMixin:
    password: tp.Annotated[str | None, Field(min_length=5, max_length=50, default=None)]


class ReadPasteSchema(PasswordMixin, BaseSchema): ...


class CreatePasteSchema(PasswordMixin, BaseSchema):
    title: tp.Annotated[str, Field(max_length=30, default="Untitled")]
    category: tp.Annotated[str | None, Field(default=None)]
    expiration: tp.Annotated[ExpirationEnum, Field(default=ExpirationEnum.NEVER)]
    text: tp.Annotated[str, at.Len(min_length=1, max_length=10_000)]

    def to_domain(self) -> CreatePasteDto:
        return CreatePasteDto(
            title=self.title,
            text=self.text,
            category=self.category,
            expiration=self.expiration,
            password=self.password,
        )


class ResponseSchema(BaseSchema):
    message: str
    data: tp.Annotated[dict | None, Field(default=None)]
