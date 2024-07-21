import typing as tp

from fastapi import APIRouter, status

from adapters.transport.rest.schemas import (
    CreatePasteSchema,
    ReadPasteSchema,
    ResponseSchema,
)
from config.ioc import container
from domain.dto.paste import CreatePasteDto, ReadPasteDto
from domain.services.paste import PasteService

router = APIRouter(prefix="/pastes")


@router.post(
    path="/{slug:str}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema,
)
async def read_paste(slug: str, schema: ReadPasteSchema):
    paste_service = container.get(PasteService)
    dto = ReadPasteDto(slug=slug, password=schema.password)
    paste = await paste_service.read(dto)

    return {
        "message": "Paste read successfully",
        "data": paste.to_dict(),
    }


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema,
)
async def create_paste(schema: CreatePasteSchema):
    paste_service = container.get(PasteService)
    dto = CreatePasteDto(**schema.model_dump(exclude_none=True))
    slug = await paste_service.create(dto)

    return {
        "message": "Paste successfully created",
        "data": {
            "slug": slug,
        },
    }
