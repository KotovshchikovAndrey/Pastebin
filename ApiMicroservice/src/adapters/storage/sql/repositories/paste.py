import typing as tp
from datetime import UTC, datetime
from sqlalchemy.sql import select, delete, update


from adapters.storage.sql.connection import SqlDatabaseConnection
from adapters.storage.sql.mappers.paste import PasteMapper
from adapters.storage.sql.models.paste import CategoryModel, PasteModel
from domain.entities.paste import Paste
from domain.ports.paste import IPasteRepository


class PasteSqlRepository(IPasteRepository):
    _database: SqlDatabaseConnection

    def __init__(self, database: SqlDatabaseConnection) -> None:
        self._database = database

    async def get_by_slug(self, slug: str) -> Paste | None:
        async with self._database.scoped_session() as session:
            stmt = select(PasteModel).where(PasteModel.slug == slug)
            model = await session.scalar(stmt)
            if model is not None:
                return PasteMapper.to_domain(model)

    async def get_popular(self, count: int = 100) -> list[Paste]:
        async with self._database.scoped_session() as session:
            stmt = select(PasteModel).order_by(PasteModel.views.desc()).limit(count)
            models = await session.scalars(stmt)
            return [PasteMapper.to_domain(model) for model in models]

    async def reset_views(self) -> None:
        async with self._database.scoped_session() as session:
            stmt = update(PasteModel).values(views=0)
            await session.execute(stmt)

    async def save(self, paste: Paste) -> None:
        model = PasteMapper.from_domain(paste)
        async with self._database.scoped_session() as session:
            stmt = select(CategoryModel).where(CategoryModel.name == paste.category)
            category = await session.scalar(stmt)
            if category is None:
                raise Exception("Invalid category")

            model.category = category
            session.add(model)

    async def increment_views(self, slug: str) -> None:
        async with self._database.scoped_session() as session:
            stmt = (
                update(PasteModel)
                .where(PasteModel.slug == slug)
                .values(views=PasteModel.views + 1)
            )

            await session.execute(stmt)

    async def delete_by_slug(self, slug: str) -> None:
        stmt = delete(PasteModel).where(PasteModel.slug == slug)
        async with self._database.scoped_session() as session:
            await session.execute(stmt)

    async def delete_expired(self) -> None:
        stmt = (
            delete(PasteModel)
            .where(PasteModel.expired_at is not None)
            .where(PasteModel.expired_at <= datetime.now(UTC).replace(tzinfo=None))
        )

        async with self._database.scoped_session() as session:
            await session.execute(stmt)
