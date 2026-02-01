from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    summary="Healthcheck",
    response_class=PlainTextResponse,
)
def ping() -> str:
    """Use sync handler to execute request call in thread."""

    return "pong"
