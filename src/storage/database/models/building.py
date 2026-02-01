from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from storage.database.models.base import Base
from storage.database.models.mixins import IdMixin

if TYPE_CHECKING:
    from . import Organization


class Building(Base, IdMixin):
    __tablename__ = "buildings"

    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    # Relationships
    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")
