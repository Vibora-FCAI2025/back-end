from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    db_uri: str

    model_config = SettingsConfigDict(env_file=".env")
