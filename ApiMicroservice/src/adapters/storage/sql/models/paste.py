import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, orm

from adapters.storage.sql.models.base import BaseModel


class CategoryModel(BaseModel):
    name: orm.Mapped[str] = orm.mapped_column(String(50), unique=True, nullable=False)


class PasteModel(BaseModel):
    __table_args__ = (
        CheckConstraint("expired_at > created_at", name="check_expired_at"),
    )

    title: orm.Mapped[str] = orm.mapped_column(String(30), nullable=False)

    slug: orm.Mapped[str] = orm.mapped_column(String(8), nullable=False, unique=True)

    text: orm.Mapped[str] = orm.mapped_column(Text, nullable=False)

    password: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)

    expired_at: orm.Mapped[datetime | None] = orm.mapped_column(DateTime, nullable=True)

    drop_after_read: orm.Mapped[bool] = orm.mapped_column(
        nullable=False,
        server_default="false",
    )

    views: orm.Mapped[int] = orm.mapped_column(
        Numeric(10, 0),
        nullable=False,
        server_default="0",
    )

    category_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
    )

    category: orm.Mapped["CategoryModel"] = orm.relationship(lazy="joined")
