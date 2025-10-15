"""
Application configuration module.

This module handles all configuration settings for the IoT Analytics Platform,
including database connection, API settings, security parameters, and logging.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/iot_analytics_db"
    )

    # API Configuration
    api_title: str = "IoT Analytics API"
    api_version: str = "1.0.0"
    api_description: str = "Real-time data analytics platform for IoT devices"

    # Security Configuration
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS Configuration
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Environment Configuration
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"

    # Logging Configuration
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings singleton instance
    """
    return Settings()
