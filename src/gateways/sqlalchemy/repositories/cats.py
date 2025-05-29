from dto import CreateCatDTO, UpdateCatDTO
from entity import Cat
from gateways.contracts import ICatsRepo
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository


class CatsRepo(SqlAlchemyRepository, ICatsRepo):
    model = Cat

    async def insert(self, dto: CreateCatDTO) -> Cat:
        return await super().create(**dto.model_dump())

    async def delete_by_id(self, cat_id: int) -> None:
        await super().delete_or_raise_not_found(id=cat_id)

    async def get_by_id(self, cat_id: int) -> Cat:
        return await super().get_one(id=cat_id)

    async def update_by_id(self, cat_id: int, dto: UpdateCatDTO) -> Cat:
        return await super().update(dto.model_dump(exclude_unset=True), id=cat_id)
