from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.base import EntityBaseModel, int_pk_type

if TYPE_CHECKING:
    from entity import Cat, Target


class Mission(EntityBaseModel):
    id: Mapped[int_pk_type]
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("cat.id", ondelete="SET NULL")
    )
    assigned_to: Mapped["Cat | None"] = relationship(back_populates="missions")
    targets: Mapped[list["Target"]] = relationship(back_populates="mission")
    # Mission can be marked as completed only when all related targets are completed
    is_completed: Mapped[bool] = mapped_column(default=False)
