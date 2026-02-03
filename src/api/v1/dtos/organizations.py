from pydantic import Field

from api.v1.dtos.activities import ActivityResponseDTO
from api.v1.dtos.base import BaseDTO, PaginatedResponseDTOMixin
from api.v1.dtos.buildings import BuildingResponseDTO


class OrganizationResponseDTO(BaseDTO):
    id: int
    name: str
    phones: list[str]

    building: BuildingResponseDTO
    activities: list[ActivityResponseDTO] = Field(default_factory=list)


class OrganizationListResponseDTO(BaseDTO, PaginatedResponseDTOMixin):
    data: list[OrganizationResponseDTO]
