import typing as tp
from abc import abstractmethod


Slug = tp.NewType("Slug", str)


class ISlugProvider(tp.Protocol):
    @abstractmethod
    async def get_unique_slug(self) -> Slug: ...

    @abstractmethod
    async def release_slug(self, slug: Slug) -> None: ...
