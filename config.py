from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    db_uri: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache  # creates only 1 object and caches it
def get_settings():
    return Settings()
