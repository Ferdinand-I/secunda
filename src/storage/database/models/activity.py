from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database.models.base import Base
from storage.database.models.mixins import IdMixin

if TYPE_CHECKING:
    from . import Organization


class Activity(Base, IdMixin):
    __tablename__ = "activities"

    name: Mapped[str]

    # Foreign keys
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("activities.id"), nullable=True)

    # Relationships
    parent: Mapped["Activity"] = relationship("Activity", remote_side="Activity.id", back_populates="children")
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent")
    # M2M
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="activities",
        secondary="organizations_activities",
    )
