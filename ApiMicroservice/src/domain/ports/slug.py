import typing as tp
from abc import abstractmethod


class ISlugProvider(tp.Protocol):
    @abstractmethod
    async def get_unique_slug(self) -> str: ...
