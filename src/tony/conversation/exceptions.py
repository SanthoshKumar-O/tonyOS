"""Conversation-related exceptions."""

from __future__ import annotations


class ConversationError(Exception):
    """Base exception for conversation errors."""


class InvalidMessageError(ConversationError):
    """Raised when an invalid message is created."""
