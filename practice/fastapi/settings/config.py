"""
Application settings loaded from environment variables.
Uses pydantic-settings for type-safe configuration management.
"""

import os
from typing import Literal
from pydantic import Field, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application settings
    service_name: str = Field(default="user-service", description="Service name")
    env: Literal["dev", "staging", "prod"] = Field(default="dev", description="Environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    
    # API settings
    api_version: str = Field(default="v1", description="API version")
    api_prefix: str = Field(default="/api", description="API prefix")
    
    # CORS settings
    cors_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS origins"
    )
    cors_allow_credentials: bool = Field(default=True, description="Allow CORS credentials")
    cors_allow_methods: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS methods"
    )
    cors_allow_headers: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS headers"
    )
    
    # Security settings
    secret_key: str = Field(
        default="change-me-in-production",
        description="Secret key for JWT/sessions"
    )
    access_token_expire_minutes: int = Field(default=30, description="JWT token expiration")
    
    # Rate limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_per_minute: int = Field(default=60, description="Requests per minute")
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="text",
        description="Log format: json or text"
    )
    
    # Database (for future use)
    database_url: str = Field(
        default="sqlite:///./app.db",
        description="Database connection URL"
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v, info):
        """Warn if using default secret key in production."""
        if info.data.get("env") == "prod" and v == "change-me-in-production":
            import warnings
            warnings.warn(
                "Using default secret key in production! Set SECRET_KEY environment variable.",
                UserWarning
            )
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "prod"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.env == "dev"


# Create singleton instance
settings = Settings()