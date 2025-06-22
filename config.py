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
    internal_jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_videos_bucket: str
    aws_default_region: str

    analysis_cli_server:str
    analysis_cli_port:str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache  # creates only 1 object and caches it
def get_settings():
    return Settings()
