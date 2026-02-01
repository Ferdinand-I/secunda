import hmac
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core.factory.exceptions import InvalidAPIKeyException
from core.settings import settings

api_key_scheme = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: Annotated[str, Depends(api_key_scheme)]) -> None:
    if not hmac.compare_digest(api_key, settings.auth.api_key.get_secret_value()):
        raise InvalidAPIKeyException


VerifyApiKey = Depends(verify_api_key)
