from entity.mission import Mission
from gateways.contracts import IMissionsRepo
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository


class MissionsRepo(SqlAlchemyRepository, IMissionsRepo):
    model = Mission

    async def get_all_and_filter(
        self,
        limit: int | None = None,
        offset: int | None = None,
        is_completed: bool | None = None,
    ):
        return await super().get_all(limit, offset, is_completed=is_completed)
