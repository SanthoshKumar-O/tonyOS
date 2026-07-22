"""Exceptions for the Context Builder."""

from __future__ import annotations


class ContextBuilderError(Exception):
    """Base exception for the Context Builder."""


class ContextBuildError(ContextBuilderError):
    """Raised when a prompt cannot be built."""
