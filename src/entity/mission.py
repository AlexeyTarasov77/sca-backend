from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.base import EntityBaseModel, int_pk_type

if TYPE_CHECKING:
    from entity import Cat, Target


class Mission(EntityBaseModel):
    id: Mapped[int_pk_type]
    assignedTo: Mapped[Cat] = relationship(back_populates="mission")
    targets: Mapped[list[Target]]
    # Mission can be marked as completed only when all related targets are completed
    is_completed: Mapped[bool] = mapped_column(default=False)
