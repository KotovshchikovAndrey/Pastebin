from dataclasses import dataclass
import typing as tp
from abc import abstractmethod


@dataclass(frozen=True, kw_only=True)
class CachedValue:
    key: str
    data: str


class ICacheSystem(tp.Protocol):
    @abstractmethod
    async def get(self, key: str) -> str | None: ...

    @abstractmethod
    async def add(self, cached_value: CachedValue) -> None: ...

    @abstractmethod
    async def add_many(self, cached_values: list[CachedValue]) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def clear(self) -> None: ...
