"""Application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "Mobile Detailing CRM"
    database_url: str = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/mobile_detailing_crm"
    app_secret_key: str = "change-me"
    demo_admin_email: str = "admin@example.com"
    demo_employee_email: str = "employee@example.com"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
