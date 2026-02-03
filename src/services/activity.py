from collections import defaultdict
from typing import Sequence

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dtos.activities import ActivityResponseDTO
from storage.database.repos.activity import SQLAlchemyActivityRepo


class ActivityService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = SQLAlchemyActivityRepo(session)

    async def get_organization_activities(
        self,
        activity_ids: Sequence[int],
        max_activity_depth: int,
    ) -> list[ActivityResponseDTO]:
        actitvity_parents = await self.repo.fetch_parents(activity_ids)

        filtered_ids = self._filter_activity_roots(
            activity_ids,
            actitvity_parents,
            max_activity_depth,
        )

        activities = await self.repo.get_nested_activities(filtered_ids, max_activity_depth)

        return self._build_tree(activities, filtered_ids)

    def _filter_activity_roots(
        self,
        ids: Sequence[int],
        rows: Sequence[Row[tuple[int, int, int]]],
        max_activity_depth: int,
    ) -> Sequence[int]:
        parents_map = self._build_parents_map(rows)

        roots = []

        for id_ in ids:
            if not any(
                root in parents_map.get(id_, {}) and parents_map[id_][root] <= max_activity_depth
                for root in roots
            ):
                roots.append(id_)

        return roots

    @staticmethod
    def _build_parents_map(rows: Sequence[Row[tuple[int, int, int]]]) -> dict:
        parents_map: dict[int, dict[int, int]] = defaultdict(dict)

        for row in rows:
            parents_map[row.id][row.parent_id] = row.pos

        return dict(parents_map)

    @staticmethod
    def _build_tree(activities: Sequence[Row[tuple]], ids: Sequence[int]) -> list[ActivityResponseDTO]:
        nodes: dict[int, ActivityResponseDTO] = {
            row.id: ActivityResponseDTO(id=row.id, name=row.name) for row in activities
        }

        children_map: dict[int, list[int]] = {}

        for row in activities:
            if row.parent_id is not None:
                children_map.setdefault(row.parent_id, []).append(row.id)

        def attach_children(node: ActivityResponseDTO) -> None:
            for child_id in children_map.get(node.id, []):
                child_node = nodes[child_id]
                attach_children(child_node)
                node.children.append(child_node)

        forest: list[ActivityResponseDTO] = []

        for id_ in ids:
            root_node = nodes[id_]
            attach_children(root_node)
            forest.append(root_node)

        return forest
