from fastapi import HTTPException
from fastapi import status


class InvalidAPIKeyException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is invalid",
            headers={"WWW-Authenticate": "X-API-Key"},
        )


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
