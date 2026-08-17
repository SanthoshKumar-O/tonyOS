"""Configuration models."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

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


class OllamaConfig(BaseModel):
    """Configuration for the Ollama provider."""

    model_config = ConfigDict(frozen=True)

    host: str = "http://127.0.0.1:11434"
    model: str = "qwen3:8b"
    timeout: int = 120


class PersistenceConfig(BaseModel):
    """Configuration for local persistence."""

    model_config = ConfigDict(frozen=True)

    database_path: Path = Path("data/tony.db")


class TonyConfiguration(BaseModel):
    """Root configuration object."""

    model_config = ConfigDict(frozen=True)

    application: ApplicationConfig = ApplicationConfig()
    logging: LoggingConfig = LoggingConfig()
    ollama: OllamaConfig = OllamaConfig()
    persistence: PersistenceConfig = PersistenceConfig()
