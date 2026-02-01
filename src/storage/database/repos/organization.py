from storage.database.models import Organization
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyActivityRepo(SQLAlchemyRepository[Organization]): ...
