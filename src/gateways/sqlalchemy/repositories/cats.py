from entity.cat import Cat
from gateways.sqlalchemy.repositories.base import SqlAlchemyRepository


class CatsRepo(SqlAlchemyRepository):
    model = Cat
