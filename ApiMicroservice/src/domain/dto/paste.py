from dataclasses import asdict, dataclass, field
from datetime import datetime
from domain.config.enums import ExpirationEnum


@dataclass(frozen=True, kw_only=True)
class CreatePasteDto:
    title: str = field(default="Untitled")
    category: str | None = field(default=None)
    password: str | None = field(default=None)
    expiration: ExpirationEnum = field(default=ExpirationEnum.NEVER)
    text: str


@dataclass(frozen=True, kw_only=True)
class ReadPasteDto:
    slug: str
    password: str = field(default="")


@dataclass(frozen=True, kw_only=True)
class PasteDto:
    title: str
    text: str
    created_at: datetime
    expired_at: datetime
    category: str

    def to_dict(self) -> dict:
        return asdict(self)
