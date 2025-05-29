from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from entity.base import EntityBaseModel, int_pk_type
from decimal import Decimal

if TYPE_CHECKING:
    from entity import Mission


class Cat(EntityBaseModel):
    id: Mapped[int_pk_type]
    name: Mapped[str]
    experience_years: Mapped[int]
    breed_name: Mapped[str]
    salary: Mapped[Decimal]
    missions: Mapped[list[Mission]]
