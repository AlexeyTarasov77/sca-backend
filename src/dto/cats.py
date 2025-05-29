from decimal import Decimal

from pydantic import Field
from dto.base import BaseDTO


class BaseCatDTO(BaseDTO):
    name: str
    experience_years: int
    salary: Decimal = Field(ge=0)
    breed_name: str


class CatDTO(BaseCatDTO):
    id: int


class CreateCatDTO(BaseCatDTO): ...


class UpdateCatDTO(BaseDTO):
    salary: Decimal = Field(ge=0)
