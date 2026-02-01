from storage.database.models import Building
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyBuildingRepo(SQLAlchemyRepository[Building]): ...
