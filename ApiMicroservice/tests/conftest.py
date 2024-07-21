from datetime import datetime
import pytest

from domain.entities.paste import Paste


@pytest.fixture
def paste() -> Paste:
    return Paste(
        slug="0",
        title="Untitled",
        text="somethong...",
        created_at=datetime(2024, 7, 21),
    )
