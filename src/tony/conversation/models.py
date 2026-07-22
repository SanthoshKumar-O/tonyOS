"""Conversation models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

from tony.conversation.exceptions import InvalidMessageError


class MessageRole(StrEnum):
    """Roles supported by the conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """A single immutable conversation message."""

    model_config = ConfigDict(frozen=True)

    role: MessageRole
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        """Ensure message content is not empty."""
        if not value.strip():
            raise InvalidMessageError("Message content cannot be empty.")
        return value


class Conversation(BaseModel):
    """Immutable conversation."""

    model_config = ConfigDict(frozen=True)

    messages: tuple[Message, ...] = ()

    def add(self, message: Message) -> Conversation:
        """Return a new conversation with an added message."""
        return Conversation(messages=self.messages + (message,))

    def system_prompt(self) -> Message | None:
        """Return the first system message if present."""
        for message in self.messages:
            if message.role is MessageRole.SYSTEM:
                return message
        return None

    def last_message(self) -> Message | None:
        """Return the most recent message."""
        if not self.messages:
            return None
        return self.messages[-1]

    def message_count(self) -> int:
        """Return the number of messages."""
        return len(self.messages)
