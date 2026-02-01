from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.settings import settings


# noinspection PyTypeChecker
def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
