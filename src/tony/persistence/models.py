"""Persistence models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class PersistenceConfig(BaseModel):
    """Configuration for local persistence."""

    model_config = ConfigDict(frozen=True)

    database_path: Path
