from datetime import UTC, datetime, timedelta
import typing as tp
import annotated_types as at
from pydantic import Field
from domain.config.enums import ExpirationEnum
from domain.entities.base import BaseEntity
import bcrypt


class Paste(BaseEntity):
    slug: tp.Annotated[str, at.MaxLen(8)]
    title: tp.Annotated[str, at.MaxLen(30)]
    text: tp.Annotated[str, at.MaxLen(1000)]
    password: tp.Annotated[str | None, Field(default=None)]
    created_at: tp.Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
    expired_at: tp.Annotated[datetime | None, Field(default=None)]
    drop_after_read: tp.Annotated[bool, Field(default=False)]
    category: tp.Annotated[str | None, Field(default=None)]

    def set_password(self, password: str) -> None:
        hashed_password = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
        self.password = hashed_password.decode()

    def check_password(self, password: str) -> bool:
        if self.password is None:
            return True

        return bcrypt.checkpw(password.encode(), hashed_password=self.password.encode())

    def set_expiration(self, expiration: ExpirationEnum) -> None:
        if expiration == ExpirationEnum.NEVER:
            self.expired_at = None
            return

        if expiration == ExpirationEnum.DROP_AFTER_READ:
            self.drop_after_read = True
            return

        self.expired_at = self.created_at + timedelta(seconds=expiration)

    def check_expired(self) -> bool:
        if self.expired_at is None:
            return False

        return datetime.now(UTC) >= self.expired_at
