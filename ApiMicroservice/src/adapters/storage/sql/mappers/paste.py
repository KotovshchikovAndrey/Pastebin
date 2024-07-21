from datetime import UTC

from adapters.storage.sql.models.paste import PasteModel
from domain.entities.paste import Paste


class PasteMapper:
    @staticmethod
    def to_domain(model: PasteModel) -> Paste:
        return Paste(
            id=model.id.hex,
            slug=model.slug,
            title=model.title,
            text=model.text,
            password=model.password,
            created_at=model.created_at.replace(tzinfo=UTC),
            drop_after_read=model.drop_after_read,
            category=model.category.name if model.category is not None else None,
            expired_at=(
                model.expired_at.replace(tzinfo=UTC)
                if model.expired_at is not None
                else None
            ),
        )

    @staticmethod
    def from_domain(entity: Paste) -> PasteModel:
        return PasteModel(
            id=entity.id,
            slug=entity.slug,
            title=entity.title,
            text=entity.text,
            password=entity.password,
            created_at=entity.created_at.replace(tzinfo=None),
            drop_after_read=entity.drop_after_read,
            expired_at=(
                entity.expired_at.replace(tzinfo=None)
                if entity.expired_at is not None
                else None
            ),
        )
