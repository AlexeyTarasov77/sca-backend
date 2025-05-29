from abc import ABC, abstractmethod

from dto import (
    CreateCatDTO,
    CreateMissionDTO,
    CreateTargetNoteDTO,
    AssignMissionDTO,
    UpdateCatDTO,
)
from entity import Cat, Mission, TargetNote, Target
from gateways.contracts import ICatsAPIClient, ICatsRepo, IMissionsRepo, ITargetsRepo


class ICatsService(ABC):
    def __init__(self, cats_repo: ICatsRepo, cats_api: ICatsAPIClient):
        self._cats_repo = cats_repo
        self._cats_api = cats_api

    @abstractmethod
    async def create_cat(self, dto: CreateCatDTO) -> Cat: ...

    @abstractmethod
    async def remove_cat(self, cat_id: int) -> None: ...

    @abstractmethod
    async def get_cat_by_id(self, cat_id: int) -> Cat: ...

    @abstractmethod
    async def get_all_cats(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Cat]: ...

    @abstractmethod
    async def update_cat(self, cat_id: int, dto: UpdateCatDTO) -> Cat: ...


class IMissionsService(ABC):
    def __init__(
        self,
        missions_repo: IMissionsRepo,
        cats_repo: ICatsRepo,
        targets_repo: ITargetsRepo,
    ):
        self._missions_repo = missions_repo
        self._cats_repo = cats_repo
        self._targets_repo = targets_repo

    @abstractmethod
    async def create_mission(self, dto: CreateMissionDTO) -> Mission: ...

    @abstractmethod
    async def remove_mission(self, mission_id: int) -> None: ...

    @abstractmethod
    async def complete_target(self, target_id: int) -> tuple[Target, bool]: ...

    @abstractmethod
    async def add_note_for_target(self, dto: CreateTargetNoteDTO) -> TargetNote: ...

    @abstractmethod
    async def assign_mission_to_cat(self, dto: AssignMissionDTO) -> Mission: ...

    @abstractmethod
    async def get_mission_by_id(self, mission_id: int) -> Mission: ...

    @abstractmethod
    async def get_all_missions(
        self,
        limit: int | None = None,
        offset: int | None = None,
        is_completed: bool | None = None,
    ) -> list[Mission]: ...
