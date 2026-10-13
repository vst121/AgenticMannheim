
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    overpass_url: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str

    typesafe_api_key: str | None = None
    typesafe_model: str = "jev-latest"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
