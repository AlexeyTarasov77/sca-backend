from abc import ABC, abstractmethod

from dto import CreateCatDTO
from entity import Cat


class ICatsRepo(ABC):
    @abstractmethod
    async def insert(self, dto: CreateCatDTO) -> Cat: ...

    @abstractmethod
    async def delete(self, cat_id: int) -> None: ...


class ICatsAPIClient(ABC):
    @abstractmethod
    async def get_all_breeds(self) -> list[str]: ...
