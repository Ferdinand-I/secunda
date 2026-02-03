from api.dependencies.db import Session
from services.organization import OrganizationCRUD


def get_organization_crud_service(session: Session) -> OrganizationCRUD:
    return OrganizationCRUD(session)
