from fastapi import APIRouter, status

from api.v1.dtos.organizations import OrganizationResponseDTO, OrganizationListResponseDTO

router = APIRouter()


@router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    summary="Get organization by id",
    response_model=OrganizationResponseDTO,
)
async def get_organization(organization_id: int) -> OrganizationResponseDTO: ...


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get filtered organizations",
    response_model=OrganizationListResponseDTO,
)
async def get_organizations() -> OrganizationListResponseDTO: ...
