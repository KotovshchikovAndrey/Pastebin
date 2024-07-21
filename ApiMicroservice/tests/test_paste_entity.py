from datetime import datetime
import pytest
from domain.config.enums import ExpirationEnum
from domain.entities.paste import Paste


class TestPasteEntity:
    @pytest.mark.parametrize(
        "slug, title, text, password",
        (
            ("1", "Untitled", "something", "12345"),
            ("2", "Some Title", "s", "password"),
            ("3TX", "T", "something...", "|12345678|"),
        ),
    )
    def test_create_paste_success(
        self, slug: str, title: str, text: str, password: str | None
    ) -> None:
        paste = Paste(slug=slug, title=title, text=text)
        assert paste.slug == slug
        assert paste.title == title
        assert paste.text == text
        assert paste.id is not None
        assert paste.created_at is not None
        assert paste.password is None

        paste.set_password(password)
        assert paste.password is not None

    @pytest.mark.parametrize(
        "expiration, expired_at, drop_after_read",
        (
            (ExpirationEnum.NEVER, None, False),
            (ExpirationEnum.DROP_AFTER_READ, None, True),
            (ExpirationEnum.ONE_MONTH, datetime(2024, 8, 21), False),
        ),
    )
    def teste_set_expiration(
        self,
        paste: Paste,
        expiration: ExpirationEnum,
        expired_at: datetime | None,
        drop_after_read: bool,
    ) -> None:
        paste.set_expiration(expiration)

        assert paste.expired_at == expired_at
        assert paste.drop_after_read == drop_after_read

    @pytest.mark.parametrize(
        "password",
        ("", None, "s s"),
    )
    def test_set_incorrent_password(self, paste: Paste, password: str | None) -> None:
        with pytest.raises(ValueError):
            paste.set_password(password)

    def test_check_password(self, paste: Paste) -> None:
        incorrect_password = "nnsnnnak"
        correct_password = "12345"

        assert paste.password is None
        assert paste.check_password(None) is True

        paste.set_password(correct_password)
        assert paste.check_password(None) is False
        assert paste.check_password(incorrect_password) is False
