from entity.mission import Mission
from gateways.contracts import IMissionsRepo
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository
from dto import PaginationDTO


class MissionsRepo(SqlAlchemyRepository, IMissionsRepo):
    model = Mission

    async def get_all_and_filter(
        self,
        pagination: PaginationDTO | None = None,
        is_completed: bool | None = None,
    ):
        return await super().get_all(pagination, is_completed=is_completed)
