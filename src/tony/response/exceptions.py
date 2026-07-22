"""Exceptions for the response system."""

from __future__ import annotations


class ResponseError(Exception):
    """Base exception for the response system."""


class ResponseGenerationError(ResponseError):
    """Raised when a response cannot be generated."""
