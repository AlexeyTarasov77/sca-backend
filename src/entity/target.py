from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.base import EntityBaseModel, int_pk_type, created_at_type


class Target(EntityBaseModel):
    id: Mapped[int_pk_type]
    name: Mapped[str]
    country_name: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(server_default="false")
    notes: Mapped[list["TargetNote"]]


class TargetNote(EntityBaseModel):
    id: Mapped[int_pk_type]
    text: Mapped[str]
    created_at: Mapped[created_at_type]
    target: Mapped[Target] = relationship(back_populates="notes")
