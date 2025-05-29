from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.base import EntityBaseModel, int_pk_type, created_at_type
from entity import Mission


class Target(EntityBaseModel):
    id: Mapped[int_pk_type]
    name: Mapped[str]
    country_name: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(server_default="false")
    mission_id: Mapped[int] = mapped_column(
        ForeignKey("mission.id", ondelete="CASCADE")
    )
    mission: Mapped[Mission] = relationship()
    notes: Mapped[list["TargetNote"]] = relationship(back_populates="target")


class TargetNote(EntityBaseModel):
    id: Mapped[int_pk_type]
    text: Mapped[str]
    created_at: Mapped[created_at_type]
    target_id: Mapped[int] = mapped_column(ForeignKey("target.id", ondelete="CASCADE"))
    target: Mapped[Target] = relationship(back_populates="notes")
