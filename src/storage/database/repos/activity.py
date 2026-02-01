from storage.database.models import Activity
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyActivityRepo(SQLAlchemyRepository[Activity]): ...
