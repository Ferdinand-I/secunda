from typing import Sequence

from sqlalchemy import select, Row, literal, CTE
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import MAX_ACTIVITY_DEPTH
from storage.database.models import Activity
from storage.database.repos.base import SQLAlchemyRepository


class SQLAlchemyActivityRepo(SQLAlchemyRepository[Activity]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Activity)

    @staticmethod
    def get_parents_tree_cte(ids: Sequence[int]) -> CTE:
        anchor = (
            select(
                Activity.id.label("activity_id"),
                Activity.parent_id,
                literal(1).label("parent_pos"),
            )
            .where(Activity.id.in_(ids))
            .where(Activity.parent_id.isnot(None))
        )

        cte = anchor.cte(name="parents", recursive=True)

        recursive = select(
            cte.c.activity_id, Activity.parent_id, (cte.c.parent_pos + 1).label("parent_pos")
        ).join(Activity, Activity.id == cte.c.parent_id)

        cte = cte.union_all(recursive)

        return cte

    @staticmethod
    def get_children_tree_cte(ids: Sequence[int], max_activity_depth: int = MAX_ACTIVITY_DEPTH) -> CTE:
        anchor = select(
            Activity.id.label("id"),
            Activity.parent_id,
            Activity.name,
            literal(1).label("level"),
        ).where(Activity.id.in_(ids))

        cte = anchor.cte(name="children", recursive=True)

        recursive = (
            select(
                Activity.id,
                Activity.parent_id,
                Activity.name,
                (cte.c.level + 1).label("level"),
            )
            .join(Activity, Activity.parent_id == cte.c.id)
            .where(cte.c.level + 1 <= max_activity_depth)
        )

        cte = cte.union_all(recursive)

        return cte

    async def fetch_parents(self, ids: Sequence[int]) -> Sequence[Row[tuple[int, int, int]]]:
        cte = self.get_parents_tree_cte(ids)

        query = select(
            cte.c.activity_id.label("id"),
            cte.c.parent_id.label("parent_id"),
            cte.c.parent_pos.label("pos"),
        )

        result = await self.session.execute(query)

        return result.all()

    async def get_nested_activities(
        self,
        ids: Sequence[int],
        max_activity_depth: int,
    ) -> Sequence[Row[tuple[int, int, str, int]]]:
        cte = self.get_children_tree_cte(ids, max_activity_depth)

        query = select(
            cte.c.id.label("id"),
            cte.c.parent_id.label("parent_id"),
            cte.c.name.label("name"),
            cte.c.level.label("level"),
        )

        result = await self.session.execute(query)

        return result.all()
