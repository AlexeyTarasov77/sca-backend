from typing import Annotated
from fastapi import APIRouter, HTTPException, status

from core.ioc import Inject
from dto import (
    MissionDTO,
    PaginationDTO,
    CreateMissionDTO,
    CreateTargetNoteDTO,
    AssignMissionDTO,
    PaginatedResponse,
    TargetNoteDTO,
    TargetDTO,
)
from dto.base import BaseDTO
from services.contracts import IMissionsService
from services.exceptions import (
    CatNotFoundError,
    InvalidOperationError,
    InvalidTargetsCount,
    MissionNotFoundError,
    TargetNotFoundError,
)


router = APIRouter(prefix="/missions")
MissionsService = Annotated[IMissionsService, Inject(IMissionsService)]


class CompleteTargetResponse(BaseDTO):
    target: TargetDTO
    mission_completed: bool


class GetMissionResponse(MissionDTO):
    targets: list[TargetDTO]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new mission",
    description="Create a new mission with optional cat assignment",
    responses={
        201: {"description": "Mission created successfully"},
        400: {"description": "Invalid cat ID or targets count"},
    },
)
async def create_mission(dto: CreateMissionDTO, service: MissionsService) -> MissionDTO:
    try:
        mission = await service.create_mission(dto)
        return MissionDTO.model_validate(mission)
    except CatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cat with ID {dto.assigned_to_id} not found",
        )
    except InvalidTargetsCount as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.msg,
        )


@router.get(
    "/",
    summary="List all missions",
    description="Get a list of all missions with optional filtering and pagination",
)
async def list_missions(
    service: MissionsService,
    pagination: PaginationDTO | None = None,
    is_completed: bool | None = None,
) -> PaginatedResponse:
    missions, total = await service.get_all_missions(pagination, is_completed)
    return PaginatedResponse.new_response(
        [MissionDTO.model_validate(mission) for mission in missions], total, pagination
    )


@router.get(
    "/{mission_id}",
    summary="Get mission by ID",
    description="Retrieve a specific mission by its ID",
    responses={
        200: {"description": "Mission retrieved successfully"},
        404: {"description": "Mission not found"},
    },
)
async def get_mission(mission_id: int, service: MissionsService) -> GetMissionResponse:
    try:
        mission = await service.get_mission_by_id(mission_id)
        return GetMissionResponse.model_validate(mission)
    except MissionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found",
        )


@router.delete(
    "/{mission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete mission",
    description="Delete a mission if it's not assigned to any cat",
    responses={
        204: {"description": "Mission deleted successfully"},
        404: {"description": "Mission not found"},
        400: {"description": "Cannot delete assigned mission"},
    },
)
async def delete_mission(mission_id: int, service: MissionsService):
    try:
        await service.remove_mission(mission_id)
    except MissionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found",
        )
    except InvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.msg,
        )


@router.patch(
    "/assign",
    summary="Assign mission to cat",
    description="Assign a mission to a cat if the cat has no active missions",
    responses={
        200: {"description": "Mission assigned successfully"},
        404: {"description": "Mission or cat not found"},
        400: {"description": "Cat already has an active mission"},
    },
)
async def assign_mission(dto: AssignMissionDTO, service: MissionsService) -> MissionDTO:
    try:
        mission = await service.assign_mission_to_cat(dto)
        return MissionDTO.model_validate(mission)
    except MissionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {dto.mission_id} not found",
        )
    except CatNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {dto.cat_id} not found",
        )
    except InvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.msg,
        )


@router.patch(
    "/targets/{target_id}/complete",
    summary="Complete target",
    description="Mark a target as completed and check if mission is completed",
    responses={
        200: {"description": "Target completed successfully"},
        404: {"description": "Target not found"},
    },
)
async def complete_target(
    target_id: int, service: MissionsService
) -> CompleteTargetResponse:
    try:
        target, is_mission_completed = await service.complete_target(target_id)
        return CompleteTargetResponse(
            target=TargetDTO.model_validate(target),
            mission_completed=is_mission_completed,
        )
    except TargetNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with ID {target_id} not found",
        )


@router.post(
    "/targets/notes",
    status_code=status.HTTP_201_CREATED,
    summary="Add note to target",
    description="Add a note to a specific target",
    responses={
        201: {"description": "Note added successfully"},
        404: {"description": "Target not found"},
    },
)
async def add_target_note(
    dto: CreateTargetNoteDTO, service: MissionsService
) -> TargetNoteDTO:
    try:
        note = await service.add_note_for_target(dto)
        return TargetNoteDTO.model_validate(note)
    except TargetNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with ID {dto.target_id} not found",
        )
    except InvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.msg,
        )
