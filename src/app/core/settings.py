from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JargerAgent(BaseModel):
    """Параметры подключения Jaeger."""
    
    jaeger_host: str
    jaeger_port: str


class ServiceUrl(BaseModel):
    """Настройки."""

    auth: str
    transaction: str
    verification: str

    root_prefix: str


class Settings(BaseSettings):
    """Настройки."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    url: ServiceUrl
    jaeger_agent: JargerAgent


settings = Settings()
