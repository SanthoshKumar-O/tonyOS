"""Exceptions for the prompt system."""

from __future__ import annotations


class PromptError(Exception):
    """Base exception for prompt-related errors."""


class PromptNotFoundError(PromptError):
    """Raised when a prompt file cannot be found."""


class PromptValidationError(PromptError):
    """Raised when a prompt file is invalid."""
