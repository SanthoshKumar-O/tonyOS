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
    ollama: OllamaConfig


class OllamaConfig(BaseModel):
    """Configuration for the Ollama provider.

    Attributes:
        host: Base URL of the Ollama server.
        model: Name of the model to use for generation.
        timeout: Request timeout, in seconds.
    """

    host: str = "http://127.0.0.1:11434"
    model: str = "qwen3:8b"
    timeout: int = 120
