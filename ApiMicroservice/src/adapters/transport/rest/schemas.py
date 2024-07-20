import typing as tp
import annotated_types as at
from pydantic import BaseModel, Field

from domain.config.enums import ExpirationEnum
from domain.dto.paste import CreatePasteDto, ReadPasteDto


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        frozen = True


class CreatePasteSchema(BaseSchema):
    title: tp.Annotated[str, Field(max_length=30, default="Untitled")]
    category: tp.Annotated[str | None, Field(default=None)]
    password: tp.Annotated[str | None, Field(default=None)]
    expiration: tp.Annotated[ExpirationEnum, Field(default=ExpirationEnum.NEVER)]
    text: tp.Annotated[str, at.MaxLen(10_000)]

    def to_domain(self) -> CreatePasteDto:
        return CreatePasteDto(
            title=self.title,
            text=self.text,
            category=self.category,
            expiration=self.expiration,
            password=self.password,
        )


class ReadPasteSchema(BaseSchema):
    slug: tp.Annotated[str, at.MaxLen(8)]
    password: tp.Annotated[str, Field(min_length=5, max_length=50, default="")]

    def to_domain(self) -> ReadPasteDto:
        return ReadPasteDto(password=self.password, slug=self.slug)


class ResponseSchema(BaseSchema):
    message: str
    data: tp.Annotated[dict | None, Field(default=None)]
