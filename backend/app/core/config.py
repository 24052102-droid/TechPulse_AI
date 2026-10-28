import os
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "TechPulse AI (ATIP)"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite:///{PROJECT_ROOT}/techpulse.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_FEED_CACHE_TTL: int = 300  # 5 minutes
    
    # External APIs
    ANTHROPIC_API_KEY: str = ""
    GITHUB_PAT: str = ""
    SEMANTIC_SCHOLAR_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*",
    ]

    # Directories
    ROOT_DIR: Path = PROJECT_ROOT
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    REPORTS_DIR: Path = PROJECT_ROOT / "ml_reports"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
