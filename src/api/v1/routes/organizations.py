from typing import Annotated

from fastapi import APIRouter, status, Depends, Query

from api.dependencies.getters import get_organization_crud_service
from api.v1.dtos.organizations import OrganizationResponseDTO, OrganizationListResponseDTO
from core.constants import MAX_ACTIVITY_DEPTH
from services.organization import OrganizationCRUD

router = APIRouter()


@router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    summary="Get organization by id",
    response_model=OrganizationResponseDTO,
)
async def get_organization(
    organization_id: int,
    service: Annotated[OrganizationCRUD, Depends(get_organization_crud_service)],
    max_activity_depth: Annotated[int, Query(ge=1, le=5)] = MAX_ACTIVITY_DEPTH,
) -> OrganizationResponseDTO:
    return await service.get_one(organization_id, max_activity_depth)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get filtered organizations",
    response_model=OrganizationListResponseDTO,
)
async def get_organizations() -> OrganizationListResponseDTO: ...
