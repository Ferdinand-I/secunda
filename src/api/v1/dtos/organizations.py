from api.v1.dtos.activities import ActivitiyResponseDTO
from api.v1.dtos.base import BaseDTO, PaginatedResponseDTOMixin
from api.v1.dtos.buildings import BuildingResponseDTO


class OrganizationResponseDTO(BaseDTO):
    id: int
    name: str
    phones: list[str]

    building: BuildingResponseDTO
    activities: list[ActivitiyResponseDTO]


class OrganizationListResponseDTO(BaseDTO, PaginatedResponseDTOMixin):
    data: list[OrganizationResponseDTO]
