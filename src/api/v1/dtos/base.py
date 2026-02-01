from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field: to_camel(field),
        populate_by_name=True,
        from_attributes=True,
    )


class PaginatedResponseDTOMixin:
    total: int
    limit: int
    offset: int
