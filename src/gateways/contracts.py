from abc import ABC, abstractmethod

from dto import CreateCatDTO, UpdateCatDTO
from entity import Cat


class ICatsRepo(ABC):
    @abstractmethod
    async def insert(self, dto: CreateCatDTO) -> Cat: ...

    @abstractmethod
    async def delete(self, cat_id: int) -> None: ...

    @abstractmethod
    async def get_by_id(self, cat_id: int) -> Cat: ...

    @abstractmethod
    async def update_by_id(self, cat_id: int, dto: UpdateCatDTO) -> Cat: ...

    @abstractmethod
    async def get_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Cat]: ...


class ICatsAPIClient(ABC):
    @abstractmethod
    async def get_all_breeds(self) -> list[str]: ...
