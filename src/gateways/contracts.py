from abc import ABC, abstractmethod

from dto import (
    CreateCatDTO,
    UpdateCatDTO,
    CreateMissionDTO,
    CreateTargetNoteDTO,
    PaginationResT,
    PaginationDTO,
)
from entity import Cat, Mission, TargetNote, Target


class ICatsRepo(ABC):
    @abstractmethod
    async def insert(self, dto: CreateCatDTO) -> Cat: ...

    @abstractmethod
    async def delete_by_id(self, cat_id: int) -> None: ...

    @abstractmethod
    async def get_by_id(self, cat_id: int) -> Cat: ...

    @abstractmethod
    async def update_by_id(self, cat_id: int, dto: UpdateCatDTO) -> Cat: ...

    @abstractmethod
    async def get_all(
        self, pagination: PaginationDTO | None = None
    ) -> PaginationResT[Cat]: ...


class ICatsAPIClient(ABC):
    @abstractmethod
    async def get_all_breeds(self) -> list[str]: ...


class IMissionsRepo(ABC):
    @abstractmethod
    async def insert(self, dto: CreateMissionDTO) -> Mission: ...

    @abstractmethod
    async def get_by_id_with_targets(self, mission_id: int) -> Mission: ...

    @abstractmethod
    async def get_by_id(self, mission_id: int) -> Mission: ...

    @abstractmethod
    @abstractmethod
    async def get_by_assigned_id(self, assigned_to_id: int) -> Mission: ...

    @abstractmethod
    async def delete_by_id(self, mission_id: int) -> None: ...

    @abstractmethod
    async def update_by_id(self, mission_id: int, **data) -> Mission: ...

    @abstractmethod
    async def get_all_and_filter(
        self,
        pagination: PaginationDTO | None = None,
        is_completed: bool | None = None,
    ) -> PaginationResT[Mission]: ...


class ITargetsRepo(ABC):
    @abstractmethod
    async def create_note(self, dto: CreateTargetNoteDTO) -> TargetNote: ...

    @abstractmethod
    async def update_by_id(self, target_id: int, **data) -> Target: ...

    @abstractmethod
    async def get_by_mission_id(self, mission_id: int) -> list[Target]: ...
    @abstractmethod
    async def get_by_id(self, target_id: int) -> Target: ...
