from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from utils.sa_error_parsers.integrity import SQLAlchemyIntegrityErrorParser


def sqlalchemy_integrity_error_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": SQLAlchemyIntegrityErrorParser(exc).parse()},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(IntegrityError, sqlalchemy_integrity_error_handler)
