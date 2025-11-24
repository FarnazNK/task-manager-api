"""Application configuration and settings."""
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = "Task Manager API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./test.db",
        description="Database connection URL"
    )
    
    # Security settings
    SECRET_KEY: str = Field(
        default="change-this-to-a-random-secret-key-in-production-min-32-chars",
        min_length=32,
        description="Secret key for JWT encoding (must be 32+ characters)"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password settings
    PWD_MIN_LENGTH: int = 8
    PWD_REQUIRE_UPPERCASE: bool = True
    PWD_REQUIRE_NUMBERS: bool = True
    PWD_REQUIRE_SPECIAL: bool = True
    
    # CORS settings - stored as string, parsed to list
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1,*"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure secret key is strong enough."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    def get_allowed_hosts(self) -> List[str]:
        """Get allowed hosts as a list."""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",") if host.strip()]


settings = Settings()