"""Clarification models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ClarificationRequest(BaseModel):
    """A request asking the user for more information."""

    model_config = ConfigDict(
        frozen=True,
    )

    question: str
