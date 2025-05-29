from entity.mission import Mission
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository


class MissionsRepo(SqlAlchemyRepository):
    model = Mission
