"""Application main router."""

from fastapi import APIRouter

from api.healthcheck import router as healthcheck_router
from api.v1.router import router as v1_router

router = APIRouter(prefix="/api")

router.include_router(router=v1_router)
router.include_router(router=healthcheck_router, tags=["Healthcheck"])
