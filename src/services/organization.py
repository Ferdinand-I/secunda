from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dtos.organizations import OrganizationResponseDTO
from core.factory.exceptions import NotFoundException
from services.activity import ActivityService
from storage.database.repos.organization import SQLAlchemyOrganizationRepo


class OrganizationCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = SQLAlchemyOrganizationRepo(session)

    async def get_one(self, id_: int, max_activity_depth: int) -> OrganizationResponseDTO:
        organization = await self.repo.get(id_)

        if not organization:
            raise NotFoundException

        response = OrganizationResponseDTO.model_construct(
            id=organization.id,
            name=organization.name,
            phones=organization.phones,
            building=organization.building,
        )

        activities = await ActivityService(session=self.repo.session).get_organization_activities(
            activity_ids=[a.id for a in organization.activities],
            max_activity_depth=max_activity_depth,
        )

        response.activities = activities

        return response
