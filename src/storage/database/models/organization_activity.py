from sqlalchemy import Table, Column, ForeignKey

from storage.database.models.base import Base

organization_activity = Table(
    "organizations_activities",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)
