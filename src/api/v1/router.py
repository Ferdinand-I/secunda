"""V1 router."""

from fastapi import APIRouter

from api.dependencies.auth import VerifyApiKey

router = APIRouter(prefix="/v1", dependencies=[VerifyApiKey])  # Verify API Key on all `v1` endpoints
