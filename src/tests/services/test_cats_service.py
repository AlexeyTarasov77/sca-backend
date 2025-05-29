from decimal import Decimal
from typing import cast
from random import randint
from faker import Faker
import pytest
from unittest.mock import Mock, create_autospec

from dto import CreateCatDTO
from entity import Cat
from gateways.contracts import ICatsAPIClient, ICatsRepo
from services.cats import CatsService
from services.exceptions import InvalidCatBreedError


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
