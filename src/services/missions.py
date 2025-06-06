from dto import CreateMissionDTO, CreateTargetNoteDTO, AssignMissionDTO, PaginationDTO
from entity import Mission, Target, TargetNote
from services.exceptions import (
    InvalidTargetsCount,
    MissionNotFoundError,
    TargetNotFoundError,
    CatNotFoundError,
    InvalidOperationError,
)
from gateways.exceptions import StorageInvalidRefError, StorageNotFoundError
from services.contracts import IMissionsService


class MissionsService(IMissionsService):
    async def create_mission(self, dto: CreateMissionDTO) -> Mission:
        if len(dto.targets) < 1 or len(dto.targets) > 3:
            raise InvalidTargetsCount()
        try:
            return await self._missions_repo.insert(dto)
        except StorageInvalidRefError:
            raise CatNotFoundError()

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        try:
            return await self._missions_repo.get_by_id_with_targets(mission_id)
        except StorageNotFoundError:
            raise MissionNotFoundError()

    async def get_all_missions(
        self,
        pagination: PaginationDTO | None = None,
        is_completed: bool | None = None,
    ):
        return await self._missions_repo.get_all_and_filter(
            pagination,
            is_completed=is_completed,
        )

    async def remove_mission(self, mission_id: int) -> None:
        try:
            mission = await self._missions_repo.get_by_id(mission_id)
            if mission.assigned_to_id is not None:
                raise InvalidOperationError(
                    "Mission can't be removed because it's already assigned"
                )
        except StorageNotFoundError:
            raise MissionNotFoundError()
        await self._missions_repo.delete_by_id(mission_id)

    async def assign_mission_to_cat(self, dto: AssignMissionDTO) -> Mission:
        """Assigns a cat to a mission.
        Cat can only be assigned to one incompleted mission at a time"""
        try:
            mission = await self._missions_repo.get_by_assigned_id(dto.cat_id)
        except StorageNotFoundError:
            pass
        else:
            if not mission.is_completed:
                raise InvalidOperationError(
                    "You can't assign cat to that mission because it's already completed"
                )
        try:
            return await self._missions_repo.update_by_id(
                dto.mission_id, assigned_to_id=dto.cat_id
            )
        except StorageNotFoundError:
            raise MissionNotFoundError()
        except StorageInvalidRefError:
            raise CatNotFoundError()

    async def complete_target(self, target_id: int) -> tuple[Target, bool]:
        """If after target completion all missions targets
        become completed - mark mission as completed too
        Returns: tuple where first value is updated target and second is boolean value
        indicating whether mission was completed"""
        try:
            updated_target = await self._targets_repo.update_by_id(
                target_id, is_completed=True
            )
        except StorageNotFoundError:
            raise TargetNotFoundError()
        mission_id = updated_target.mission_id
        all_targets_for_mission = await self._targets_repo.get_by_mission_id(mission_id)
        if all(target.is_completed for target in all_targets_for_mission):
            await self._missions_repo.update_by_id(mission_id, is_completed=True)
            return updated_target, True
        return updated_target, False

    async def add_note_for_target(self, dto: CreateTargetNoteDTO) -> TargetNote:
        try:
            target = await self._targets_repo.get_by_id(dto.target_id)
        except StorageNotFoundError:
            raise TargetNotFoundError()
        if target.is_completed:
            raise InvalidOperationError(
                "Target notes are 'frozen' because target is already completed"
            )
        return await self._targets_repo.create_note(dto)
