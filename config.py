from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    db_uri: str

    smtp_server: str
    smtp_port: str
    sender_email: str
    sender_password: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache  # creates only 1 object and caches it
def get_settings():
    return Settings()
