import typing as tp
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class SqlDatabaseConnection:
    _engine: AsyncEngine
    _scoped_session: async_scoped_session[AsyncSession]

    def __init__(self, url: str, echo: bool = False) -> None:
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_maker = async_sessionmaker(
            self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def scoped_session(self) -> tp.AsyncIterator[AsyncSession]:
        scoped_session = self._get_scoped_session()
        async with scoped_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as exc:
                await session.rollback()
                raise
            finally:
                await scoped_session.remove()

    async def close(self) -> None:
        await self._engine.dispose()

    def _get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        scoped_session = async_scoped_session(
            self._session_maker,
            scopefunc=current_task,
        )

        return scoped_session
