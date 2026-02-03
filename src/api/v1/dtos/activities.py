from pydantic import Field

from api.v1.dtos.base import BaseDTO


class ActivityResponseDTO(BaseDTO):
    id: int
    name: str

    children: list["ActivityResponseDTO"] = Field(alias="subActivities", default_factory=list)
