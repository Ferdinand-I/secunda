from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from storage.database.models import Organization, Activity
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyOrganizationRepo(SQLAlchemyRepository[Organization]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Organization)

    async def get(self, id_: int) -> Organization | None:
        stmt = select(self.model).where(and_(self.model.id == id_))

        stmt = stmt.options(
            joinedload(Organization.activities).load_only(Activity.id),
            joinedload(Organization.building),
        )

        result = await self.session.execute(stmt)

        return result.unique().scalar_one_or_none()
