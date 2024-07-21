import asyncio

from domain.dto.paste import CreatePasteDto, PasteDto, ReadPasteDto
from domain.entities.paste import Paste
from domain.exceptions.paste import InvalidPasswordException, PasteNotFoundException
from domain.ports.cache import ICacheSystem
from domain.ports.paste import IPasteRepository
from domain.ports.slug import ISlugProvider, Slug


class PasteService:
    _repository: IPasteRepository
    _cache: ICacheSystem
    _slug: ISlugProvider

    def __init__(
        self,
        repository: IPasteRepository,
        cache: ICacheSystem,
        slug: ISlugProvider,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._slug = slug

    async def read(self, dto: ReadPasteDto) -> PasteDto:
        cached_paste = await self._cache.get(dto.slug)
        if cached_paste is not None:
            paste = Paste.model_validate_json(cached_paste)
        else:
            paste = await self._repository.get_by_slug(dto.slug)
            if paste is None:
                raise PasteNotFoundException()

        if paste.check_expired():
            raise PasteNotFoundException()

        if not paste.check_password(dto.password):
            raise InvalidPasswordException()

        output = PasteDto(
            category=paste.category,
            title=paste.title,
            text=paste.text,
            created_at=paste.created_at,
            expired_at=paste.expired_at,
        )

        if paste.drop_after_read:
            await self._repository.delete_by_slug(paste.slug)
            await self._slug.release_slug(paste.slug)
            return output

        coro = self._repository.increment_views(paste.slug)
        asyncio.create_task(coro)
        return output

    async def create(self, dto: CreatePasteDto) -> Slug:
        new_paste = Paste(
            slug=await self._slug.get_unique_slug(),
            title=dto.title,
            category=dto.category,
            text=dto.text,
        )

        new_paste.set_expiration(expiration=dto.expiration)
        if dto.password is not None:
            new_paste.set_password(dto.password)

        await self._repository.save(new_paste)
        return new_paste.slug
