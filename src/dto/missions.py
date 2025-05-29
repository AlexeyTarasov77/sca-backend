from typing import Optional
from pydantic import BaseModel


class CreateTargetDTO(BaseModel):
    name: str
    country_name: str


class CreateMissionDTO(BaseModel):
    assigned_to_id: Optional[int] = None
    targets: list[CreateTargetDTO]


class CreateTargetNoteDTO(BaseModel):
    text: str
    target_id: int


class AssignMissionDTO(BaseModel):
    mission_id: int
    cat_id: int
