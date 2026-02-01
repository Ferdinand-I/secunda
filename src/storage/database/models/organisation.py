from typing import TYPE_CHECKING

from sqlalchemy import String, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database.models.base import Base
from storage.database.models.mixins import IdMixin

if TYPE_CHECKING:
    from . import Activity, Building


class Organization(Base, IdMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    phones: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)

    # Foreign keys
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id", ondelete="CASCADE"))

    # Relationships
    building: Mapped[list["Building"]] = relationship("Building", back_populates="organizations")
    # M2M
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="organizations",
        secondary="organizations_activities",
    )
