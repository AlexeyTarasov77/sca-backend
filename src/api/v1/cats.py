from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status

from core.ioc import Inject
from dto import (
    CreateCatDTO,
    CatDTO,
    PaginatedResponse,
    PaginationDTO,
    EntityIDParam,
    UpdateCatDTO,
)
from services.contracts import ICatsService
from services.exceptions import CatNotFoundError, InvalidCatBreedError


router = APIRouter(prefix="/cats", tags=["cats"])

CatsService = Annotated[ICatsService, Inject(ICatsService)]


@router.post(
    "/",
    response_model=CatDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new cat",
    description="Create a new spy cat with validation for breed",
    responses={
        201: {"description": "Cat created successfully"},
        400: {"description": "Invalid cat breed or validation error"},
    },
)
async def create_cat(dto: CreateCatDTO, service: CatsService) -> CatDTO:
    try:
        cat = await service.create_cat(dto)
        return CatDTO.model_validate(cat)

    except InvalidCatBreedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cat breed: {dto.breed_name}",
        )


@router.get(
    "/",
    summary="List all cats",
    description="Get a list of all cats with optional pagination",
)
async def list_cats(
    service: CatsService, pagination: PaginationDTO | None = None
) -> PaginatedResponse:
    cats, total = await service.get_all_cats(pagination)
    return PaginatedResponse.new_response(
        [CatDTO.model_validate(cat) for cat in cats], total, pagination
    )


@router.get(
    "/{cat_id}",
    summary="Get cat by ID",
    description="Retrieve a specific cat by its ID",
)
async def get_cat(
    service: CatsService,
    cat_id: int = Path(ge=1),
) -> CatDTO:
    try:
        cat = await service.get_cat_by_id(cat_id)
        return CatDTO.model_validate(cat)
    except CatNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.msg,
        )


@router.put(
    "/{cat_id}",
    response_model=CatDTO,
    summary="Update cat",
    description="Update an existing cat's information",
)
async def update_cat(
    cat_id: EntityIDParam,
    service: CatsService,
    dto: UpdateCatDTO,
) -> CatDTO:
    try:
        if not dto.model_dump(exclude_unset=True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )

        cat = await service.update_cat(cat_id, dto)
        return CatDTO.model_validate(cat)

    except CatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {cat_id} not found",
        )


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete cat",
    description="Delete a cat by ID",
    responses={
        204: {"description": "Cat deleted successfully"},
        404: {"description": "Cat not found"},
    },
)
async def delete_cat(cat_id: EntityIDParam, service: CatsService):
    try:
        await service.remove_cat(cat_id)

    except CatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {cat_id} not found",
        )
