"""Protocols for conversation services."""

from __future__ import annotations

from typing import Protocol

from tony.conversation.models import Conversation


class ConversationServiceProtocol(Protocol):
    """Conversation interface."""

    def reply(
        self,
        conversation: Conversation,
        user_message: str,
    ) -> Conversation: ...
