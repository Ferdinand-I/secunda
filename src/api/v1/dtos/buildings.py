from api.v1.dtos.base import BaseDTO


class BuildingResponseDTO(BaseDTO):
    id: int
    address: str
    latitude: float
    longitude: float
