from pydantic_settings import SettingsConfigDict, BaseSettings


class DatabaseSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_username: str
    postgres_password: str
    postgres_db: str


class CacheSettings(BaseSettings):
    redis_url: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    database: DatabaseSettings
    cache: CacheSettings
