from dto import CreateCatDTO
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
            await self._cats_repo.delete(cat_id)
        except StorageNotFoundError:
            raise CatNotFoundError()
