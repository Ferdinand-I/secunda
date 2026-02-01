"""Application main router."""

from fastapi import APIRouter

from api.v1.router import router as v1_router

router = APIRouter(prefix="/api")

router.include_router(router=v1_router)
