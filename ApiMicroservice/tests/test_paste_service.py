import pytest
from unittest.mock import AsyncMock
from domain.config.enums import ExpirationEnum
from domain.dto.paste import ReadPasteDto
from domain.entities.paste import Paste
from domain.exceptions.paste import InvalidPasswordException
from domain.ports.cache import ICacheSystem
from domain.ports.paste import IPasteRepository
from domain.ports.slug import ISlugProvider
from domain.services.paste import PasteService


class TestePasteService:
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock(spec=IPasteRepository)

    @pytest.fixture
    def mock_cache(self):
        return AsyncMock(spec=ICacheSystem)

    @pytest.fixture
    def mock_slug(self):
        return AsyncMock(spec=ISlugProvider)

    @pytest.mark.parametrize("valid_password", ("12345", "12345678", "something"))
    async def test_read_when_send_valid_password(
        self,
        mock_repository: AsyncMock,
        mock_cache: AsyncMock,
        mock_slug: AsyncMock,
        paste: Paste,
        valid_password: str,
    ) -> None:
        paste.set_password(valid_password)
        mock_repository.get_by_slug.return_value = paste
        mock_repository.increment_views.return_value = None
        mock_cache.get.return_value = None

        paste_service = PasteService(
            repository=mock_repository,
            cache=mock_cache,
            slug=mock_slug,
        )

        dto = ReadPasteDto(slug=paste.slug, password=valid_password)
        response = await paste_service.read(dto)
        assert response is not None

    @pytest.mark.parametrize("invalid_password", ("", "12345678", None))
    async def test_read_when_send_invalid_password(
        self,
        mock_repository: AsyncMock,
        mock_cache: AsyncMock,
        mock_slug: AsyncMock,
        paste: Paste,
        invalid_password: str | None,
    ) -> None:
        valid_password = "12345"
        paste.set_password(valid_password)

        mock_repository.get_by_slug.return_value = paste
        mock_repository.increment_views.return_value = None
        mock_cache.get.return_value = None

        paste_service = PasteService(
            repository=mock_repository,
            cache=mock_cache,
            slug=mock_slug,
        )

        dto = ReadPasteDto(slug=paste.slug, password=invalid_password)
        with pytest.raises(InvalidPasswordException):
            await paste_service.read(dto)

    async def test_read_from_cache(
        self,
        mock_repository: AsyncMock,
        mock_cache: AsyncMock,
        mock_slug: AsyncMock,
        paste: Paste,
    ) -> None:
        mock_cache.get.return_value = paste.model_dump_json()
        mock_repository.get_by_slug.return_value = paste
        mock_repository.increment_views.return_value = None

        paste_service = PasteService(
            repository=mock_repository,
            cache=mock_cache,
            slug=mock_slug,
        )

        dto = ReadPasteDto(slug=paste.slug)
        response = await paste_service.read(dto)

        assert response is not None
        mock_cache.get.assert_called_once_with(paste.slug)
        mock_repository.get_by_slug.assert_not_called()

    async def test_increment_views(
        self,
        mock_repository: AsyncMock,
        mock_cache: AsyncMock,
        mock_slug: AsyncMock,
        paste: Paste,
    ) -> None:
        mock_cache.get.return_value = paste.model_dump_json()
        mock_repository.get_by_slug.return_value = paste
        mock_repository.increment_views.return_value = None

        paste_service = PasteService(
            repository=mock_repository,
            cache=mock_cache,
            slug=mock_slug,
        )

        dto = ReadPasteDto(slug=paste.slug)
        await paste_service.read(dto)
        mock_repository.increment_views.assert_called_once_with(paste.slug)

    async def test_increment_views_not_called_when_drop_after_read(
        self,
        mock_repository: AsyncMock,
        mock_cache: AsyncMock,
        mock_slug: AsyncMock,
        paste: Paste,
    ) -> None:
        paste.set_expiration(expiration=ExpirationEnum.DROP_AFTER_READ)

        mock_cache.get.return_value = paste.model_dump_json()
        mock_repository.get_by_slug.return_value = paste
        mock_repository.increment_views.return_value = None

        paste_service = PasteService(
            repository=mock_repository,
            cache=mock_cache,
            slug=mock_slug,
        )

        dto = ReadPasteDto(slug=paste.slug)
        await paste_service.read(dto)
        mock_repository.increment_views.assert_not_called()
