"""Prompt models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Prompt(BaseModel):
    """Represents a prompt document."""

    model_config = ConfigDict(frozen=True)

    name: str
    content: str
