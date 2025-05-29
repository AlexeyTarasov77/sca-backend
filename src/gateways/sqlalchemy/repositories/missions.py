from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from entity import Mission, Target, TargetNote
from gateways.contracts import IMissionsRepo, ITargetsRepo
from gateways.exceptions import StorageNotFoundError
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository
from dto import PaginationDTO, CreateTargetNoteDTO, CreateMissionDTO
from gateways.sqlalchemy import get_session


class MissionsRepo(SqlAlchemyRepository[Mission], IMissionsRepo):
    model = Mission

    async def get_all_and_filter(
        self,
        pagination: PaginationDTO | None = None,
        is_completed: bool | None = None,
    ):
        return await super().get_all(pagination, is_completed=is_completed)

    async def get_by_id(self, mission_id: int) -> Mission:
        return await super().get_one(id=mission_id)

    async def get_by_id_with_targets(self, mission_id: int) -> Mission:
        stmt = (
            select(self.model)
            .filter_by(id=mission_id)
            .options(selectinload(self.model.targets))
        )
        async with get_session() as session:
            res = await session.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            raise StorageNotFoundError()
        return obj

    async def insert(self, dto: CreateMissionDTO) -> Mission:
        targets = [Target(**target_dto.model_dump()) for target_dto in dto.targets]
        instance = Mission(**dto.model_dump(exclude={"targets"}), targets=targets)
        async with get_session() as session:
            session.add(instance)
            await session.flush()
        return instance

    async def get_by_assigned_id(self, assigned_to_id: int) -> Mission:
        return await super().get_one(assigned_to_id=assigned_to_id)

    async def delete_by_id(self, mission_id: int) -> None:
        await super().delete_or_raise_not_found(id=mission_id)

    async def update_by_id(self, mission_id: int, **data) -> Mission:
        return await super().update(data, id=mission_id)


class TargetsRepo(SqlAlchemyRepository[Target], ITargetsRepo):
    model = Target

    async def create_note(self, dto: CreateTargetNoteDTO) -> TargetNote:
        stmt = insert(TargetNote).values(**dto.model_dump())
        async with get_session() as session:
            res = await session.execute(stmt)
        return res.scalar_one()

    async def update_by_id(self, target_id: int, **data) -> Target:
        return await super().update(data, id=target_id)

    async def get_by_mission_id(self, mission_id: int) -> list[Target]:
        records, _ = await super().get_all(mission_id=mission_id)
        return list(records)

    async def get_by_id(self, target_id: int) -> Target:
        return await super().get_one(id=target_id)
