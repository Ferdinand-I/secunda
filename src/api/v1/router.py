"""V1 router."""

from fastapi import APIRouter

from api.dependencies.auth import VerifyApiKey
from api.v1.routes.organizations import router as organizations_router

router = APIRouter(prefix="/v1", dependencies=[VerifyApiKey])  # Verify API Key on all `v1` endpoints

router.include_router(organizations_router, prefix="/organizations", tags=["Organizations"])
