import typing as tp
from abc import abstractmethod

from domain.entities.paste import Paste


class IPasteRepository(tp.Protocol):
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Paste | None: ...

    @abstractmethod
    async def get_popular(self, count: int = 100) -> list[Paste]: ...

    @abstractmethod
    async def reset_views(self) -> None: ...

    @abstractmethod
    async def save(self, paste: Paste) -> None: ...

    @abstractmethod
    async def increment_views(self, slug: str) -> None: ...

    @abstractmethod
    async def delete_by_slug(self, slug: str) -> None: ...

    @abstractmethod
    async def delete_expired(self) -> None: ...
