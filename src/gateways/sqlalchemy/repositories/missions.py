from sqlalchemy import insert
from entity import Mission, Target, TargetNote
from gateways.contracts import IMissionsRepo, ITargetsRepo
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository
from dto import PaginationDTO, CreateTargetNoteDTO
from gateways.sqlalchemy import session_factory


class MissionsRepo(SqlAlchemyRepository[Mission], IMissionsRepo):
    model = Mission

    async def get_all_and_filter(
        self,
        pagination: PaginationDTO | None = None,
        is_completed: bool | None = None,
    ):
        return await super().get_all(pagination, is_completed=is_completed)


class TargetsRepo(SqlAlchemyRepository[Target], ITargetsRepo):
    model = Target

    async def create_note(self, dto: CreateTargetNoteDTO) -> TargetNote:
        stmt = insert(TargetNote).values(**dto.model_dump())
        async with session_factory() as session:
            res = await session.execute(stmt)
        return res.scalar_one()

    async def update_by_id(self, target_id: int, **data) -> Target:
        return await super().update(data, id=target_id)

    async def get_by_mission_id(self, mission_id: int) -> list[Target]:
        records, _ = await super().get_all(mission_id=mission_id)
        return list(records)

    async def get_by_id(self, target_id: int) -> Target:
        return await super().get_one(id=target_id)
