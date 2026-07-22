"""Execution context models."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from tony.conversation import Conversation
from tony.session import Session


class RequestContext(BaseModel):
    """Represents an incoming user request."""

    model_config = ConfigDict(frozen=True)

    user_input: str
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )


class EnvironmentContext(BaseModel):
    """Represents Tony's runtime environment."""

    model_config = ConfigDict(frozen=True)

    current_working_directory: str
    platform: str
    hostname: str
    python_version: str


class ExecutionMetadata(BaseModel):
    """Metadata attached to an execution."""

    model_config = ConfigDict(frozen=True)

    execution_id: str = Field(default_factory=lambda: str(uuid4()))
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )


class ExecutionSettings(BaseModel):
    """Runtime settings snapshot."""

    model_config = ConfigDict(frozen=True)

    provider_name: str
    temperature: float
    streaming: bool


class ExecutionContext(BaseModel):
    """Immutable snapshot of Tony's execution state."""

    model_config = ConfigDict(frozen=True)

    session: Session
    conversation: Conversation

    request: RequestContext
    environment: EnvironmentContext

    metadata: ExecutionMetadata
    settings: ExecutionSettings
