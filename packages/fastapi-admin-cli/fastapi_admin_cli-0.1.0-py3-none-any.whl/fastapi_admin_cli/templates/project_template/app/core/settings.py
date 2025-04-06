from pydantic_settings import BaseSettings
from typing import Optional, List
import logging

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "{{ project_name }} API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A FastAPI application created with fastapi-admin-cli."
    API_PORT: int = 8000
    API_DOMAIN: str = "api.yourdomain.com"

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "{{ project_name }}"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "postgres"
    DATABASE_URL: Optional[str] = None

    # Traefik Settings
    TRAEFIK_DASHBOARD_HOST: str = "traefik.yourdomain.com"
    TRAEFIK_DASHBOARD_AUTH: str = "user:password"
    ACME_EMAIL: str = "your.email@example.com"

    # Environment Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Auth Settings
    SECRET_KEY: str = "your-secret-key-here"
    JWT_SECRET: str = "your-jwt-secret-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Settings
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_FROM_NAME: str = "{{ project_name }} API"
    MAIL_TLS: bool = True      # Will be mapped to MAIL_STARTTLS in ConnectionConfig
    MAIL_SSL: bool = False     # Will be mapped to MAIL_SSL_TLS in ConnectionConfig
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    def configure_logging(self) -> None:
        """Configure logging based on environment settings."""
        log_level = getattr(logging, self.LOG_LEVEL)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
        
        # Set lower log levels for noisy libraries
        if not self.DEBUG:
            logging.getLogger("uvicorn").setLevel(logging.WARNING)
            logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
