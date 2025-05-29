from collections.abc import Sequence
import math
from pydantic import BaseModel, Field, computed_field


class BaseDTO(BaseModel):
    class Config:
        from_attributes = True


class PaginationDTO(BaseDTO):
    limit: int = Field(default=10, gt=0, lt=100)
    offset: int = Field(default=0, ge=0)


type PaginationResT[R] = tuple[Sequence[R], int]


class PaginatedResponse[T: BaseDTO](PaginationDTO):
    objects: Sequence[T]
    total_records: int
    first_page: int = 1

    @computed_field()
    @property
    def last_page(self) -> int:
        return math.ceil(self.total_records / self.limit)

    @classmethod
    def new_response(
        cls,
        objects: Sequence[T],
        total_records: int,
        pagination_dto: PaginationDTO,
    ):
        return cls(
            objects=objects,
            total_records=total_records,
            first_page=1,
            **pagination_dto.model_dump(),
        )
