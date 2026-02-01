from typing import Optional
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    # WARNING: Default contains placeholder credentials - MUST be changed in production!
    # Set DATABASE_URL environment variable with your actual database credentials
    database_url: str = "postgresql+psycopg://finapp:finapp@localhost:5432/finapp"
    
    # API
    api_prefix: str = "/api/v1"
    project_name: str = "FinApp"
    version: str = "0.1.0"
    
    # Security
    # WARNING: Default is a placeholder - MUST be changed in production!
    # Generate a secure key: python -c "import secrets; print(secrets.token_urlsafe(32))"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    # Comma-separated list of allowed origins for CORS
    cors_origins: str = "*"  # WARNING: Set to specific origins in production!
    
    # Plaid Integration
    plaid_client_id: str = ""
    plaid_secret: str = ""
    plaid_environment: str = "sandbox"  # sandbox, development, or production
    plaid_redirect_uri: str = "http://localhost:3000/plaid/callback"
    
    class Config:
        env_file = ".env"
    
    def get_cors_origins(self) -> list:
        """Get CORS origins as a list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()

# Validate production settings
def validate_production_settings():
    """Validate that production settings are not using defaults"""
    import os
    
    # Only validate if explicitly in production mode
    if os.getenv("ENVIRONMENT") == "production":
        if settings.secret_key == "your-secret-key-here-change-in-production":
            raise ValueError(
                "SECRET_KEY must be changed in production! "
                "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        
        if "finapp:finapp" in settings.database_url:
            raise ValueError(
                "DATABASE_URL contains default credentials and must be changed in production!"
            )
        
        if settings.cors_origins == "*":
            raise ValueError(
                "CORS_ORIGINS must be set to specific origins in production!"
            )
        
        if not settings.plaid_client_id or not settings.plaid_secret:
            raise ValueError(
                "PLAID_CLIENT_ID and PLAID_SECRET must be set in production!"
            )

# Run validation
validate_production_settings()
