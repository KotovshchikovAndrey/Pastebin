import typing as tp
import annotated_types as at
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    host: str
    port: tp.Annotated[int, at.Gt(0)]
    worker_count: tp.Annotated[int, Field(gt=0, default=1)]
    is_debug: bool = True


class DatabaseSettings(BaseModel):
    postgres_url: str
    echo: bool = True


class CacheSettings(BaseModel):
    memcached_host: str
    memcached_port: int
    ttl: int = 60 * 60 * 24  # 1 day


class BackgroundSettings(BaseModel):
    broker_url: str


class ProviderSettings(BaseModel):
    slug_address: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    server: ServerSettings
    database: DatabaseSettings
    cache: CacheSettings
    background: BackgroundSettings
    provider: ProviderSettings
