"""Exceptions for the tools system."""

from __future__ import annotations


class ToolError(Exception):
    """Base exception for the tools system."""


class ToolRegistrationError(ToolError):
    """Raised when tool registration fails."""


class ToolDiscoveryError(ToolError):
    """Raised when tool discovery fails."""


class ToolValidationError(ToolError):
    """Raised when tool arguments are invalid."""


class ToolPermissionError(ToolError):
    """Raised when tool execution is not permitted."""


class ToolExecutionError(ToolError):
    """Raised when tool execution fails."""
