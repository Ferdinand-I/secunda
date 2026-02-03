from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Sequence

from sqlalchemy import select, and_, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, entity: T) -> T: ...

    @abstractmethod
    async def get(self, id_: int) -> T | None: ...

    @abstractmethod
    async def remove(self, id_: int) -> int: ...

    @abstractmethod
    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = settings.api.limit,
        offset: int = settings.api.offset,
    ) -> Sequence[T]: ...


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()

        return entity

    async def get(self, id_: int) -> T | None:
        result = await self.session.execute(select(self.model).where(and_(self.model.id == id_)))

        return result.scalar_one_or_none()

    async def remove(self, id_: int) -> int:
        result: Result = await self.session.execute(delete(self.model).where(and_(self.model.id == id_)))
        await self.session.flush()

        return result.rowcount  # type: ignore[attr-defined]

    async def list(
        self,
        filters=None,
        limit=settings.api.limit,
        offset=settings.api.offset,
    ) -> Sequence[T]:
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)

        return result.scalars().all()
