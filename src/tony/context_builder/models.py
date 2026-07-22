"""Context Builder models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PromptBuildResult(BaseModel):
    """Represents the result of building a prompt."""

    model_config = ConfigDict(frozen=True)

    prompt: str
