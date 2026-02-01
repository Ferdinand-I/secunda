from fastapi import FastAPI

from api.router import router
from core.factory.exception_handlers import setup_exception_handlers
from core.factory.middlewares import setup_middlewares


def build_app() -> FastAPI:
    """FastAPI app builder."""

    app = FastAPI()

    app.include_router(router)
    setup_middlewares(app)
    setup_exception_handlers(app)

    return app
