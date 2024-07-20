from adapters.storage.sql.models.paste import PasteModel
from domain.entities.paste import Paste


class PasteMapper:
    @staticmethod
    def to_domain(model: PasteModel) -> Paste:
        return Paste(
            id=model.id,
            slug=model.slug,
            title=model.title,
            text=model.text,
            password=model.password,
            category=model.category.name,
            created_at=model.created_at,
            drop_after_read=model.drop_after_read,
            expired_at=model.expired_at,
        )

    @staticmethod
    def from_domain(entity: Paste) -> PasteModel:
        return PasteModel(
            id=entity.id,
            slug=entity.slug,
            title=entity.title,
            text=entity.text,
            password=entity.password,
            created_at=entity.created_at,
            drop_after_read=entity.drop_after_read,
            expired_at=entity.expired_at,
        )
