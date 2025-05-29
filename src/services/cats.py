from dto import CreateCatDTO, UpdateCatDTO, PaginationDTO
from entity import Cat
from gateways.exceptions import StorageNotFoundError
from services.contracts import ICatsService
from services.exceptions import CatNotFoundError, InvalidCatBreedError


class CatsService(ICatsService):
    async def create_cat(self, dto: CreateCatDTO) -> Cat:
        valid_breeds = await self._cats_api.get_all_breeds()
        if dto.breed_name.lower() not in [breed.lower() for breed in valid_breeds]:
            raise InvalidCatBreedError()
        return await self._cats_repo.insert(dto)

    async def remove_cat(self, cat_id: int) -> None:
        try:
            await self._cats_repo.delete_by_id(cat_id)
        except StorageNotFoundError:
            raise CatNotFoundError()

    async def get_cat_by_id(self, cat_id: int) -> Cat:
        try:
            return await self._cats_repo.get_by_id(cat_id)
        except StorageNotFoundError:
            raise CatNotFoundError()

    async def get_all_cats(
        self,
        pagination: PaginationDTO | None = None,
    ):
        return await self._cats_repo.get_all(pagination)

    async def update_cat(self, cat_id: int, dto: UpdateCatDTO) -> Cat:
        try:
            return await self._cats_repo.update_by_id(cat_id, dto)
        except StorageNotFoundError:
            raise CatNotFoundError()
