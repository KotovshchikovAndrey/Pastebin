import uuid
from datetime import datetime

from sqlalchemy import DateTime, orm, text
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(orm.DeclarativeBase):
    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime,
        nullable=False,
        server_default=text("TIMEZONE('UTC', NOW())"),
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()
