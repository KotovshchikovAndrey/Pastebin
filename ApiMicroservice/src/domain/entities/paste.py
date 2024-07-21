import typing as tp
from datetime import UTC, datetime, timedelta

import annotated_types as at
import bcrypt
from pydantic import Field

from domain.config.enums import ExpirationEnum
from domain.entities.base import BaseEntity


class Paste(BaseEntity):
    slug: tp.Annotated[str, at.Len(min_length=1, max_length=8)]
    title: tp.Annotated[str, at.Len(min_length=1, max_length=30)]
    text: tp.Annotated[str, at.Len(min_length=1, max_length=10_000)]
    password: tp.Annotated[str | None, Field(default=None)]
    created_at: tp.Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
    expired_at: tp.Annotated[datetime | None, Field(default=None)]
    drop_after_read: tp.Annotated[bool, Field(default=False)]
    category: tp.Annotated[str | None, Field(default=None)]

    def set_password(self, password: str) -> None:
        if not password:
            raise ValueError("Invalid password value. Excpected the NOT EMPTY string")

        if password.count(" ") != 0:
            raise ValueError(
                "Invalid password value. Excpected the string without spaces"
            )

        hashed_password = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
        self.password = hashed_password.decode()

    def check_password(self, password: str | None) -> bool:
        if self.password is None:
            return True

        if password is None:
            return False

        return bcrypt.checkpw(password.encode(), hashed_password=self.password.encode())

    def set_expiration(self, expiration: ExpirationEnum) -> None:
        if (expiration != ExpirationEnum.NEVER) and (
            expiration != ExpirationEnum.DROP_AFTER_READ
        ):
            self.expired_at = self.created_at + timedelta(seconds=expiration)
            return

        self.expired_at = None
        self.drop_after_read = expiration == ExpirationEnum.DROP_AFTER_READ

    def check_expired(self) -> bool:
        if self.expired_at is None:
            return False

        return datetime.now(UTC) >= self.expired_at
