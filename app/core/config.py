"""Configuration centralisée via Pydantic Settings v2."""
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Variables d'environnement et configuration de l'application."""

    # Projet
    PROJECT_NAME: str = "Xweto Backend API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "production", "test"] = "development"

    # Sécurité
    SECRET_KEY: str = Field(..., description="Clé secrète pour JWT (env var SECRET_KEY)")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Base de données PostgreSQL (async)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/xweto",
        description="Connexion async PostgreSQL (asyncpg driver)",
    )
    DATABASE_ECHO: bool = False  # Log les requêtes SQL en debug

    # Paiements
    FEDAPAY_API_KEY: str = Field(default="", description="Clé API Fedapay")
    FEDAPAY_ENV: Literal["development", "production"] = "development"

    # OCR / IA
    OCR_PROVIDER_API_KEY: str = Field(default="", description="Clé API pour OCR (ex: Google Vision)")

    # Notifications multicanal
    SMS_PROVIDER_API_KEY: str = Field(default="", description="Clé API SMS (ex: Twilio)")
    EMAIL_PROVIDER_API_KEY: str = Field(default="", description="Clé API Email (ex: SendGrid)")

    class Config:
        """Configuration Pydantic v2."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instance unique (singleton)
settings = Settings()
