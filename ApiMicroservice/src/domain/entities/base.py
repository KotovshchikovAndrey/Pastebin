import typing as tp
from abc import ABC
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseEntity(ABC, BaseModel):
    id: tp.Annotated[str, Field(default_factory=lambda: uuid4().hex)]

    class Config:
        from_attributes = True
        validate_assignment = True

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseEntity):
            return False

        return self.id == value.id
