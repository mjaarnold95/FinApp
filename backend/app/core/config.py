from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://finapp:finapp@localhost:5432/finapp"
    
    # API
    api_prefix: str = "/api/v1"
    project_name: str = "FinApp"
    version: str = "0.1.0"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()
