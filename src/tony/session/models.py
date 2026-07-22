"""Session models."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from tony.conversation import Conversation


class SessionMetadata(BaseModel):
    """Metadata associated with a session."""

    model_config = ConfigDict(frozen=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Session(BaseModel):
    """Represents a conversation session."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)

    title: str = "New Chat"

    conversation: Conversation = Field(default_factory=Conversation)

    metadata: SessionMetadata = Field(default_factory=SessionMetadata)

    def with_conversation(
        self,
        conversation: Conversation,
    ) -> Session:
        """Return a new session with an updated conversation."""

        return self.model_copy(
            update={
                "conversation": conversation,
                "metadata": self.metadata.model_copy(
                    update={
                        "updated_at": datetime.now(UTC),
                    }
                ),
            }
        )
