from decimal import Decimal
from typing import cast
from random import randint
from faker import Faker
import pytest
from unittest.mock import Mock, create_autospec

from dto import CreateCatDTO, UpdateCatDTO, PaginationDTO
from entity import Cat
from gateways.contracts import ICatsAPIClient, ICatsRepo
from gateways.exceptions import StorageNotFoundError
from services.cats import CatsService
from services.exceptions import CatNotFoundError, InvalidCatBreedError


class MockedCatsService(CatsService):
    """Redeclares mocked attributes types for type checking purposes"""

    _cats_repo: Mock
    _cats_api: Mock


@pytest.fixture
def cats_service() -> MockedCatsService:
    mock_cats_repo = create_autospec(ICatsRepo)
    mock_cats_api = create_autospec(ICatsAPIClient)
    return cast(MockedCatsService, CatsService(mock_cats_repo, mock_cats_api))


@pytest.fixture
def fake_create_cat_dto(faker: Faker):
    return CreateCatDTO(
        name=faker.name(),
        experience_years=randint(0, 10),
        salary=Decimal(randint(0, 9999)),
        breed_name=faker.name(),
    )


@pytest.fixture
def fake_update_cat_dto():
    return UpdateCatDTO(
        salary=Decimal(randint(0, 9999)),
    )


@pytest.fixture
def fake_cat(faker: Faker):
    return Cat(
        id=randint(1, 100000),
        name=faker.name(),
        experience_years=randint(0, 10),
        salary=Decimal(randint(0, 9999)),
        breed_name=faker.name(),
    )


@pytest.mark.asyncio
class TestCatsService:
    async def test_create_cat_success(
        self, cats_service: MockedCatsService, fake_create_cat_dto: CreateCatDTO
    ):
        expected_res = Cat()
        breeds_list = [fake_create_cat_dto.breed_name]
        cats_service._cats_repo.insert.return_value = expected_res
        cats_service._cats_api.get_all_breeds.return_value = breeds_list
        res = await cats_service.create_cat(fake_create_cat_dto)
        assert res == expected_res
        cats_service._cats_repo.insert.assert_awaited_once_with(fake_create_cat_dto)
        cats_service._cats_api.get_all_breeds.assert_awaited_once()

    async def test_create_cat_invalid_breed(
        self, cats_service: MockedCatsService, fake_create_cat_dto: CreateCatDTO
    ):
        breeds_list = []
        cats_service._cats_api.get_all_breeds.return_value = breeds_list
        with pytest.raises(InvalidCatBreedError):
            await cats_service.create_cat(fake_create_cat_dto)
        cats_service._cats_repo.insert.assert_not_awaited()
        cats_service._cats_api.get_all_breeds.assert_awaited_once()

    async def test_remove_cat_sucsess(self, cats_service: MockedCatsService):
        fake_cat_id = randint(1, 100000)
        res = await cats_service.remove_cat(fake_cat_id)
        assert res is None
        cats_service._cats_repo.delete_by_id.assert_awaited_once_with(fake_cat_id)

    async def test_remove_cat_not_found(self, cats_service: MockedCatsService):
        fake_cat_id = randint(1, 100000)
        cats_service._cats_repo.delete_by_id.side_effect = StorageNotFoundError()
        with pytest.raises(CatNotFoundError):
            await cats_service.remove_cat(fake_cat_id)
        cats_service._cats_repo.delete_by_id.assert_awaited_once_with(fake_cat_id)

    async def test_get_cat_by_id_success(
        self, cats_service: MockedCatsService, fake_cat: Cat
    ):
        fake_cat_id = fake_cat.id
        cats_service._cats_repo.get_by_id.return_value = fake_cat

        res = await cats_service.get_cat_by_id(fake_cat_id)

        assert res == fake_cat
        cats_service._cats_repo.get_by_id.assert_awaited_once_with(fake_cat_id)

    async def test_get_cat_by_id_not_found(self, cats_service: MockedCatsService):
        fake_cat_id = randint(1, 100000)
        cats_service._cats_repo.get_by_id.side_effect = StorageNotFoundError()

        with pytest.raises(CatNotFoundError):
            await cats_service.get_cat_by_id(fake_cat_id)

        cats_service._cats_repo.get_by_id.assert_awaited_once_with(fake_cat_id)

    # New tests for get_all_cats
    async def test_get_all_cats_success(
        self, cats_service: MockedCatsService, fake_cat: Cat
    ):
        expected_cats = [fake_cat]
        cats_service._cats_repo.get_all.return_value = expected_cats

        res = await cats_service.get_all_cats()

        assert res == expected_cats
        cats_service._cats_repo.get_all.assert_awaited_once_with(None)

    async def test_get_all_cats_with_pagination(
        self, cats_service: MockedCatsService, fake_cat: Cat
    ):
        expected_cats = [fake_cat]
        cats_service._cats_repo.get_all.return_value = expected_cats
        pagination = PaginationDTO()
        res = await cats_service.get_all_cats(pagination)

        assert res == expected_cats
        cats_service._cats_repo.get_all.assert_awaited_once_with(pagination)

    # New tests for update_cat
    async def test_update_cat_success(
        self,
        cats_service: MockedCatsService,
        fake_cat: Cat,
        fake_update_cat_dto: UpdateCatDTO,
    ):
        fake_cat_id = fake_cat.id
        updated_cat = Cat()

        cats_service._cats_repo.get_by_id.return_value = fake_cat
        cats_service._cats_repo.update_by_id.return_value = updated_cat

        res = await cats_service.update_cat(fake_cat_id, fake_update_cat_dto)

        assert res == updated_cat
        cats_service._cats_repo.update_by_id.assert_awaited_once_with(
            fake_cat_id, fake_update_cat_dto
        )

    async def test_update_cat_not_found(
        self, cats_service: MockedCatsService, fake_update_cat_dto: UpdateCatDTO
    ):
        fake_cat_id = randint(1, 100000)
        cats_service._cats_repo.update_by_id.side_effect = StorageNotFoundError()

        with pytest.raises(CatNotFoundError):
            await cats_service.update_cat(fake_cat_id, fake_update_cat_dto)

        cats_service._cats_repo.update_by_id.assert_awaited_once_with(
            fake_cat_id, fake_update_cat_dto
        )
