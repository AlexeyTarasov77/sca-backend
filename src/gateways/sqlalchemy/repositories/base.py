from collections.abc import Mapping, Sequence
from sqlalchemy import CursorResult, Row, delete, func, insert, select, update
from dto.base import PaginationDTO, PaginationResT
from entity.base import EntityBaseModel
from gateways.sqlalchemy.main import session_factory

from gateways.exceptions import GatewayError, StorageNotFoundError


class SqlAlchemyRepository[T: EntityBaseModel]:
    model: type[T]

    # def __init__(self, session: AsyncSession) -> None:
    #     self._session = session
    #
    async def create(self, **values) -> T:
        if not values:
            raise GatewayError("No data to insert")
        stmt = insert(self.model).values(**values).returning(self.model)
        async with session_factory() as session:
            res = await session.execute(stmt)
        return res.scalars().one()

    async def save(self, instance: T):
        async with session_factory() as session:
            session.add(instance)
            await session.flush()

    async def get_one(self, **filter_by) -> T:
        stmt = select(self.model).filter_by(**filter_by).limit(1)
        async with session_factory() as session:
            res = await session.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            raise StorageNotFoundError()
        return obj

    async def update(self, data: Mapping, **filter_by) -> T:
        if not data:
            raise GatewayError("No data to update. Provided data is empty")
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data)
            .returning(self.model)
        )
        async with session_factory() as session:
            res = await session.execute(stmt)
        obj = res.scalars().one_or_none()
        if not obj:
            raise StorageNotFoundError()
        return obj

    async def delete(self, **filter_by) -> CursorResult:
        stmt = delete(self.model).filter_by(**filter_by)
        async with session_factory() as session:
            res = await session.execute(stmt)
        return res

    async def delete_or_raise_not_found(self, **filter_by) -> None:
        res = await self.delete(**filter_by)
        if res.rowcount < 1:
            raise StorageNotFoundError()

    def _split_records_and_count(
        self, res: Sequence[Row[tuple[T, int]]]
    ) -> PaginationResT[T]:
        try:
            count = res[0][1]
            records = [row[0] for row in res]
            return records, count
        except IndexError:
            return [], 0

    async def get_all(
        self, pagination: PaginationDTO | None = None, **filter_by
    ) -> PaginationResT[T]:
        stmt = select(self.model, func.count().over())
        if pagination is not None:
            stmt = stmt.offset(pagination.offset).limit(pagination.limit)
        stmt = stmt.filter_by(**filter_by)

        async with session_factory() as session:
            res = await session.execute(stmt)
        return self._split_records_and_count(res.all())
