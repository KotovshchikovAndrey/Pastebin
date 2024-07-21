import typing as tp
from datetime import datetime
from dataclasses import dataclass, field
from domain.config.enums import ExpirationEnum
from domain.dto.base import BaseDto


@dataclass(kw_only=True, frozen=True)
class ReadPasteDto(BaseDto):
    slug: str
    password: str | None = field(default=None)


@dataclass(kw_only=True, frozen=True)
class CreatePasteDto(BaseDto):
    text: str
    title: str = field(default="Untitled")
    expiration: ExpirationEnum = field(default=ExpirationEnum.NEVER)
    category: str | None = field(default=None)
    password: str | None = field(default=None)


@dataclass(kw_only=True, frozen=True)
class PasteDto(BaseDto):
    title: str
    text: str
    created_at: datetime
    expired_at: datetime | None = field(default=None)
    category: str | None = field(default=None)
