from typing import Annotated
from fastapi import APIRouter

from core.ioc import Inject
from dto import CatDTO
from services.contracts import ICatsService


router = APIRouter(prefix="/cats")

CatsService = Annotated[ICatsService, Inject(ICatsService)]


@router.get("/")
async def list_cats(service: CatsService):
    ents = await service.get_all_cats()
    return [CatDTO.model_validate(ent) for ent in ents]
