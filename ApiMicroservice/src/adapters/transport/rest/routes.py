import typing as tp
from adapters.transport.rest import schemas
from config.ioc import container
from fastapi import APIRouter, status
from domain.services.paste import PasteService

router = APIRouter(prefix="/pastes")


@router.post(
    path="/{slug:str}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseSchema,
)
async def read_paste(slug: str, schema: schemas.ReadPasteSchema):
    paste_service = container.get(PasteService)
    new_paste = await paste_service.read(slug=slug, password=schema.password)

    return {
        "message": "Paste read successfully",
        "data": new_paste.to_dict(),
    }


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseSchema,
)
async def create_paste(schema: schemas.CreatePasteSchema):
    paste_service = container.get(PasteService)
    slug = await paste_service.create(schema.to_domain())

    return {
        "message": "Paste successfully created",
        "data": {
            "slug": slug,
        },
    }
