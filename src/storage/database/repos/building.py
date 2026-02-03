from sqlalchemy.ext.asyncio import AsyncSession

from storage.database.models import Building
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyBuildingRepo(SQLAlchemyRepository[Building]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Building)
