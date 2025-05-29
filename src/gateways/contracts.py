from abc import ABC, abstractmethod

from dto import CreateCatDTO
from entity import Cat


class ICatsRepo(ABC):
    @abstractmethod
    async def insert(self, dto: CreateCatDTO) -> Cat: ...


class ICatsAPIClient(ABC):
    @abstractmethod
    async def get_all_breeds(self) -> list[str]: ...
