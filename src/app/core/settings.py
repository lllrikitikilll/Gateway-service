from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceUrl(BaseModel):
    """Настройки."""

    auth: str
    transaction: str
    verification: str


class Settings(BaseSettings):
    # Временный пример как мне испольховать APP_CONFIG__url__auth
    """Настройки."""
    
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    url: ServiceUrl


settings = Settings()
