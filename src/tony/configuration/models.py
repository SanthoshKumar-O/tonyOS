from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ApplicationConfig(BaseModel):
    """Application-related configuration."""

    model_config = ConfigDict(frozen=True)

    name: str = "Tony"
    environment: str = "development"


class LogLevel(StrEnum):
    """Supported logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseModel):
    """Logging configuration."""

    model_config = ConfigDict(frozen=True)

    level: LogLevel = LogLevel.INFO


class TonyConfiguration(BaseModel):
    """Root configuration object."""

    model_config = ConfigDict(frozen=True)

    application: ApplicationConfig = ApplicationConfig()
    logging: LoggingConfig = LoggingConfig()
