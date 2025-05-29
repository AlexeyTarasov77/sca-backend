# from typing import cast
# from random import randint
# from faker import Faker
# import pytest
# from unittest.mock import Mock, create_autospec
#
# from dto import CreateMissionDTO, CreateTargetNoteDTO, AssignMissionDTO
# from dto.missions import CreateTargetDTO
# from entity import Mission, Target, TargetNote
# from gateways.contracts import ICatsRepo, IMissionsRepo, ITargetsRepo
# from gateways.exceptions import StorageNotFoundError, StorageInvalidRefError
# from services.missions import MissionsService
# from services.exceptions import (
#     MissionNotFoundError,
#     TargetNotFoundError,
#     CatNotFoundError,
#     InvalidOperationError,
# )
#
#
# class MockedMissionsService(MissionsService):
#     """Redeclares mocked attributes types for type checking purposes"""
#
#     _cats_repo: Mock
#     _missions_repo: Mock
#     _targets_repo: Mock
#
#
# @pytest.fixture
# def missions_service() -> MockedMissionsService:
#     mock_cats_repo = create_autospec(ICatsRepo)
#     mock_missions_repo = create_autospec(IMissionsRepo)
#     mock_targets_repo = create_autospec(ITargetsRepo)
#     return cast(
#         MockedMissionsService,
#         MissionsService(mock_cats_repo, mock_missions_repo, mock_targets_repo),
#     )
#
#
# @pytest.fixture
# def fake_create_mission_dto(faker: Faker):
#     return CreateMissionDTO(
#         targets=[
#             CreateTargetDTO(name=faker.name(), country_name=faker.country())
#             for _ in range(randint(1, 3))
#         ],
#     )
#
#
# @pytest.fixture
# def fake_assign_mission_dto():
#     return AssignMissionDTO(
#         mission_id=randint(1, 100),
#         cat_id=randint(1, 100),
#     )
#
#
# @pytest.fixture
# def fake_create_target_note_dto(faker: Faker):
#     return CreateTargetNoteDTO(
#         target_id=randint(1, 100),
#         text=faker.text(),
#     )
#
#
# @pytest.fixture
# def fake_mission():
#     return Mission(
#         id=randint(1, 100000),
#         assigned_to_id=randint(1, 100),
#         is_completed=False,
#     )
#
#
# @pytest.fixture
# def fake_completed_mission():
#     return Mission(
#         id=randint(1, 100000),
#         assigned_to_id=randint(1, 100),
#         is_completed=True,
#     )
#
#
# @pytest.fixture
# def fake_unassigned_mission():
#     return Mission(
#         id=randint(1, 100000),
#         assigned_to_id=None,
#         is_completed=False,
#     )
#
#
# @pytest.fixture
# def fake_target(faker: Faker):
#     return Target(
#         id=randint(1, 100000),
#         mission_id=randint(1, 100),
#         name=faker.name(),
#         country_name=faker.country(),
#         is_completed=False,
#     )
#
#
# @pytest.fixture
# def fake_completed_target(faker: Faker):
#     return Target(
#         id=randint(1, 100000),
#         mission_id=randint(1, 100),
#         name=faker.name(),
#         country_name=faker.country(),
#         is_completed=True,
#     )
#
#
# @pytest.fixture
# def fake_target_note(faker: Faker):
#     return TargetNote(
#         id=randint(1, 100000),
#         target_id=randint(1, 100),
#         text=faker.text(),
#         created_at=faker.date_time(),
#     )
#
#
# @pytest.mark.asyncio
# class TestMissionsService:
#     async def test_create_mission_success_with_assignment(
#         self,
#         missions_service: MockedMissionsService,
#         fake_create_mission_dto: CreateMissionDTO,
#     ):
#         expected_mission = Mission()
#         missions_service._cats_repo.get_by_id.return_value = Mock()  # Cat exists
#         missions_service._missions_repo.insert.return_value = expected_mission
#
#         res = await missions_service.create_mission(fake_create_mission_dto)
#
#         assert res == expected_mission
#         missions_service._cats_repo.get_by_id.assert_awaited_once_with(
#             fake_create_mission_dto.assigned_to_id
#         )
#         missions_service._missions_repo.insert.assert_awaited_once_with(
#             fake_create_mission_dto
#         )
#
#     async def test_create_mission_success_without_assignment(
#         self,
#         missions_service: MockedMissionsService,
#         fake_create_mission_dto_no_assignment: CreateMissionDTO,
#     ):
#         expected_mission = Mission()
#         missions_service._missions_repo.insert.return_value = expected_mission
#
#         res = await missions_service.create_mission(
#             fake_create_mission_dto_no_assignment
#         )
#
#         assert res == expected_mission
#         missions_service._cats_repo.get_by_id.assert_not_awaited()
#         missions_service._missions_repo.insert.assert_awaited_once_with(
#             fake_create_mission_dto_no_assignment
#         )
#
#     async def test_create_mission_cat_not_found(
#         self,
#         missions_service: MockedMissionsService,
#         fake_create_mission_dto: CreateMissionDTO,
#     ):
#         missions_service._cats_repo.get_by_id.side_effect = StorageNotFoundError()
#
#         with pytest.raises(CatNotFoundError):
#             await missions_service.create_mission(fake_create_mission_dto)
#
#         missions_service._cats_repo.get_by_id.assert_awaited_once_with(
#             fake_create_mission_dto.assigned_to_id
#         )
#         missions_service._missions_repo.insert.assert_not_awaited()
#
#     async def test_get_mission_by_id_success(
#         self, missions_service: MockedMissionsService, fake_mission: Mission
#     ):
#         fake_mission_id = fake_mission.id
#         missions_service._missions_repo.get_by_id.return_value = fake_mission
#
#         res = await missions_service.get_mission_by_id(fake_mission_id)
#
#         assert res == fake_mission
#         missions_service._missions_repo.get_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#
#     async def test_get_mission_by_id_not_found(
#         self, missions_service: MockedMissionsService
#     ):
#         fake_mission_id = randint(1, 100000)
#         missions_service._missions_repo.get_by_id.side_effect = StorageNotFoundError()
#
#         with pytest.raises(MissionNotFoundError):
#             await missions_service.get_mission_by_id(fake_mission_id)
#
#         missions_service._missions_repo.get_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#
#     async def test_get_all_missions_success(
#         self, missions_service: MockedMissionsService, fake_mission: Mission
#     ):
#         expected_missions = [fake_mission]
#         missions_service._missions_repo.get_all.return_value = expected_missions
#
#         res = await missions_service.get_all_missions()
#
#         assert res == expected_missions
#         missions_service._missions_repo.get_all.assert_awaited_once_with(
#             limit=None, offset=None, is_completed=None
#         )
#
#     async def test_get_all_missions_with_pagination_and_filter(
#         self, missions_service: MockedMissionsService, fake_mission: Mission
#     ):
#         expected_missions = [fake_mission]
#         limit, offset, is_completed = 10, 5, True
#         missions_service._missions_repo.get_all.return_value = expected_missions
#
#         res = await missions_service.get_all_missions(
#             limit=limit, offset=offset, is_completed=is_completed
#         )
#
#         assert res == expected_missions
#         missions_service._missions_repo.get_all.assert_awaited_once_with(
#             limit=limit, offset=offset, is_completed=is_completed
#         )
#
#     async def test_delete_mission_success_unassigned(
#         self, missions_service: MockedMissionsService, fake_unassigned_mission: Mission
#     ):
#         fake_mission_id = fake_unassigned_mission.id
#         missions_service._missions_repo.get_by_id.return_value = fake_unassigned_mission
#
#         res = await missions_service.remove_mission(fake_mission_id)
#
#         assert res is None
#         missions_service._missions_repo.get_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#         missions_service._missions_repo.delete_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#
#     async def test_delete_mission_invalid_operation_assigned(
#         self, missions_service: MockedMissionsService, fake_mission: Mission
#     ):
#         fake_mission_id = fake_mission.id
#         missions_service._missions_repo.get_by_id.return_value = fake_mission
#
#         with pytest.raises(InvalidOperationError):
#             await missions_service.remove_mission(fake_mission_id)
#
#         missions_service._missions_repo.get_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#         missions_service._missions_repo.delete_by_id.assert_not_awaited()
#
#     async def test_delete_mission_not_found(
#         self, missions_service: MockedMissionsService
#     ):
#         fake_mission_id = randint(1, 100000)
#         missions_service._missions_repo.get_by_id.side_effect = StorageNotFoundError()
#
#         with pytest.raises(MissionNotFoundError):
#             await missions_service.remove_mission(fake_mission_id)
#
#         missions_service._missions_repo.get_by_id.assert_awaited_once_with(
#             fake_mission_id
#         )
#         missions_service._missions_repo.delete_by_id.assert_not_awaited()
#
#     async def test_assign_mission_to_cat_success_no_previous_assignment(
#         self,
#         missions_service: MockedMissionsService,
#         fake_assign_mission_dto: AssignMissionDTO,
#     ):
#         expected_mission = Mission()
#         missions_service._missions_repo.get_by_assigned_id.side_effect = (
#             StorageNotFoundError()
#         )
#         missions_service._missions_repo.update_by_id.return_value = expected_mission
#
#         res = await missions_service.assign_mission_to_cat(fake_assign_mission_dto)
#
#         assert res == expected_mission
#         missions_service._missions_repo.get_by_assigned_id.assert_awaited_once_with(
#             fake_assign_mission_dto.cat_id
#         )
#         missions_service._missions_repo.update_by_id.assert_awaited_once_with(
#             fake_assign_mission_dto.mission_id,
#             assigned_to_id=fake_assign_mission_dto.mission_id,
#         )
#
#     async def test_assign_mission_to_cat_success_previous_completed(
#         self,
#         missions_service: MockedMissionsService,
#         fake_assign_mission_dto: AssignMissionDTO,
#         fake_completed_mission: Mission,
#     ):
#         expected_mission = Mission()
#         missions_service._missions_repo.get_by_assigned_id.return_value = (
#             fake_completed_mission
#         )
#         missions_service._missions_repo.update_by_id.return_value = expected_mission
#
#         res = await missions_service.assign_mission_to_cat(fake_assign_mission_dto)
#
#         assert res == expected_mission
#         missions_service._missions_repo.get_by_assigned_id.assert_awaited_once_with(
#             fake_assign_mission_dto.cat_id
#         )
#         missions_service._missions_repo.update_by_id.assert_awaited_once_with(
#             fake_assign_mission_dto.mission_id,
#             assigned_to_id=fake_assign_mission_dto.mission_id,
#         )
#
#     async def test_assign_mission_to_cat_invalid_operation_uncompleted_mission(
#         self,
#         missions_service: MockedMissionsService,
#         fake_assign_mission_dto: AssignMissionDTO,
#         fake_mission: Mission,
#     ):
#         missions_service._missions_repo.get_by_assigned_id.return_value = fake_mission
#
#         with pytest.raises(InvalidOperationError):
#             await missions_service.assign_mission_to_cat(fake_assign_mission_dto)
#
#         missions_service._missions_repo.get_by_assigned_id.assert_awaited_once_with(
#             fake_assign_mission_dto.cat_id
#         )
#         missions_service._missions_repo.update_by_id.assert_not_awaited()
#
#     async def test_assign_mission_to_cat_mission_not_found(
#         self,
#         missions_service: MockedMissionsService,
#         fake_assign_mission_dto: AssignMissionDTO,
#     ):
#         missions_service._missions_repo.get_by_assigned_id.side_effect = (
#             StorageNotFoundError()
#         )
#         missions_service._missions_repo.update_by_id.side_effect = (
#             StorageNotFoundError()
#         )
#
#         with pytest.raises(MissionNotFoundError):
#             await missions_service.assign_mission_to_cat(fake_assign_mission_dto)
#
#         missions_service._missions_repo.get_by_assigned_id.assert_awaited_once_with(
#             fake_assign_mission_dto.cat_id
#         )
#         missions_service._missions_repo.update_by_id.assert_awaited_once_with(
#             fake_assign_mission_dto.mission_id,
#             assigned_to_id=fake_assign_mission_dto.mission_id,
#         )
#
#     async def test_assign_mission_to_cat_cat_not_found(
#         self,
#         missions_service: MockedMissionsService,
#         fake_assign_mission_dto: AssignMissionDTO,
#     ):
#         missions_service._missions_repo.get_by_assigned_id.side_effect = (
#             StorageNotFoundError()
#         )
#         missions_service._missions_repo.update_by_id.side_effect = (
#             StorageInvalidRefError()
#         )
#
#         with pytest.raises(CatNotFoundError):
#             await missions_service.assign_mission_to_cat(fake_assign_mission_dto)
#
#         missions_service._missions_repo.get_by_assigned_id.assert_awaited_once_with(
#             fake_assign_mission_dto.cat_id
#         )
#         missions_service._missions_repo.update_by_id.assert_awaited_once_with(
#             fake_assign_mission_dto.mission_id,
#             assigned_to_id=fake_assign_mission_dto.mission_id,
#         )
#
#     async def test_complete_target_success_mission_not_completed(
#         self, missions_service: MockedMissionsService, fake_target: Target
#     ):
#         fake_target_id = fake_target.id
#         updated_target = Target(
#             id=fake_target.id,
#             mission_id=fake_target.mission_id,
#             name=fake_target.name,
#             country_name=fake_target.country_name,
#             is_completed=True,
#         )
#         incomplete_target = Target(is_completed=False)
#         all_targets = [updated_target, incomplete_target]
#
#         missions_service._targets_repo.update_by_id.return_value = updated_target
#         missions_service._targets_repo.get_by_mission_id.return_value = all_targets
#
#         res = await missions_service.complete_target(fake_target_id)
#
#         assert res == (updated_target, False)
#         missions_service._targets_repo.update_by_id.assert_awaited_once_with(
#             fake_target_id, is_completed=True
#         )
#         missions_service._targets_repo.get_by_mission_id.assert_awaited_once_with(
#             fake_target.mission_id
#         )
#         missions_service._missions_repo.update_by_id.assert_not_awaited()
#
#     async def test_complete_target_success_mission_completed(
#         self, missions_service: MockedMissionsService, fake_target: Target
#     ):
#         fake_target_id = fake_target.id
#         updated_target = Target(
#             id=fake_target.id,
#             mission_id=fake_target.mission_id,
#             name=fake_target.name,
#             country_name=fake_target.country_name,
#             is_completed=True,
#         )
#         completed_target = Target(is_completed=True)
#         all_targets = [updated_target, completed_target]
#
#         missions_service._targets_repo.update_by_id.return_value = updated_target
#         missions_service._targets_repo.get_by_mission_id.return_value = all_targets
#
#         res = await missions_service.complete_target(fake_target_id)
#
#         assert res == (updated_target, True)
#         missions_service._targets_repo.update_by_id.assert_awaited_once_with(
#             fake_target_id, is_completed=True
#         )
#         missions_service._targets_repo.get_by_mission_id.assert_awaited_once_with(
#             fake_target.mission_id
#         )
#         missions_service._missions_repo.update_by_id.assert_awaited_once_with(
#             fake_target.mission_id, is_completed=True
#         )
#
#     async def test_complete_target_not_found(
#         self, missions_service: MockedMissionsService
#     ):
#         fake_target_id = randint(1, 100000)
#         missions_service._targets_repo.update_by_id.side_effect = StorageNotFoundError()
#
#         with pytest.raises(TargetNotFoundError):
#             await missions_service.complete_target(fake_target_id)
#
#         missions_service._targets_repo.update_by_id.assert_awaited_once_with(
#             fake_target_id, is_completed=True
#         )
#         missions_service._targets_repo.get_by_mission_id.assert_not_awaited()
#         missions_service._missions_repo.update_by_id.assert_not_awaited()
#
#     async def test_add_note_for_target_success(
#         self,
#         missions_service: MockedMissionsService,
#         fake_create_target_note_dto: CreateTargetNoteDTO,
#         fake_target_note: TargetNote,
#     ):
#         missions_service._targets_repo.create_note.return_value = fake_target_note
#
#         res = await missions_service.add_note_for_target(fake_create_target_note_dto)
#
#         assert res == fake_target_note
#         missions_service._targets_repo.create_note.assert_awaited_once_with(
#             fake_create_target_note_dto
#         )
#
#     async def test_add_note_for_target_not_found(
#         self,
#         missions_service: MockedMissionsService,
#         fake_create_target_note_dto: CreateTargetNoteDTO,
#     ):
#         missions_service._targets_repo.create_note.side_effect = (
#             StorageInvalidRefError()
#         )
#
#         with pytest.raises(TargetNotFoundError):
#             await missions_service.add_note_for_target(fake_create_target_note_dto)
#
#         missions_service._targets_repo.create_note.assert_awaited_once_with(
#             fake_create_target_note_dto
#         )
