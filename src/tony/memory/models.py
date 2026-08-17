"""Memory domain models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from tony.memory.exceptions import InvalidMemoryError


class MemoryScope(StrEnum):
    """Scopes supported by Tony's memory system."""

    WORKING = "working"
    CONVERSATION = "conversation"
    PROJECT = "project"
    WORKSPACE = "workspace"
    SEMANTIC = "semantic"


class Memory(BaseModel):
    """Represents an immutable piece of Tony's memory."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    content: str
    scope: MemoryScope
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        """Ensure memory content is not empty."""
        if not value.strip():
            raise InvalidMemoryError("Memory content cannot be empty.")
        return value


class MemoryDecision(BaseModel):
    """Represents the outcome of a memory policy decision."""

    model_config = ConfigDict(frozen=True)

    allowed: bool
    reason: str
