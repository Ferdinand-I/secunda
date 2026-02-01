"""V1 router."""

from fastapi import APIRouter

from api.v1.routes.healthcheck import router as healthcheck_router

router = APIRouter(prefix="/v1")

router.include_router(router=healthcheck_router, tags=["Healthcheck"])
