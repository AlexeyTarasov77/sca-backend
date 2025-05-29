from datetime import datetime
from dto.base import BaseDTO


class TargetDTO(BaseDTO):
    id: int
    name: str
    country_name: str
    is_completed: bool
    mission_id: int


class TargetNoteDTO(BaseDTO):
    id: int
    text: str
    created_at: datetime
    target_id: int


class CreateTargetDTO(BaseDTO):
    name: str
    country_name: str


class MissionDTO(BaseDTO):
    id: int
    assigned_to_id: int | None
    is_completed: bool


class CreateMissionDTO(BaseDTO):
    assigned_to_id: int | None = None
    targets: list[CreateTargetDTO]


class CreateTargetNoteDTO(BaseDTO):
    text: str
    target_id: int


class AssignMissionDTO(BaseDTO):
    mission_id: int
    cat_id: int
