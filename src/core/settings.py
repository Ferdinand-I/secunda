import os
from enum import StrEnum
from ipaddress import IPv4Address
from pathlib import Path
from typing import Final, Literal

from pydantic import Field, HttpUrl, SecretStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent


class Environment(StrEnum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class BaseSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env"),  # Only for out of container developing
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )


class AuthConfig(BaseModel):
    api_key: SecretStr


class APIConfig(BaseModel):
    origins: list[HttpUrl | Literal["*"]] = Field(default=["*"])


class DBConfig(BaseModel):
    # DSN
    host: str = "localhost"  # Docker DSN
    port: int = 5432
    user: str = "postgres"
    password: str
    name: str

    # Engine
    pool_size: int = 1
    max_overflow: int = 2

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


class ServerConfig(BaseModel):
    host: IPv4Address = Field(default="0.0.0.0")
    port: int = Field(gt=0, lt=65536, default=8000)
    workers: int = Field(gt=0, le=os.cpu_count() - 1)  # Limit workers depends on CPU cores
    reload: bool = True


class Settings(BaseSettingsConfig):
    environment: Environment = Environment.LOCAL
    auth: AuthConfig
    api: APIConfig
    server: ServerConfig
    db: DBConfig


settings = Settings()  # noqa
