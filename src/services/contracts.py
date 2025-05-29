from abc import ABC, abstractmethod

from dto import CreateCatDTO
from entity import Cat
from gateways.contracts import ICatsAPIClient, ICatsRepo


class ICatsService(ABC):
    def __init__(self, cats_repo: ICatsRepo, cats_api: ICatsAPIClient):
        self._cats_repo = cats_repo
        self._cats_api = cats_api

    @abstractmethod
    async def create_cat(self, dto: CreateCatDTO) -> Cat: ...
