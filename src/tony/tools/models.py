"""Tool models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ToolCapability(StrEnum):
    """Capabilities supported by a tool."""

    FILESYSTEM = "filesystem"
    SHELL = "shell"
    GIT = "git"
    PYTHON = "python"
    NETWORK = "network"
    SYSTEM = "system"


class ToolMetadata(BaseModel):
    """Describes a registered tool."""

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    capability: ToolCapability


class ToolArgument(BaseModel):
    """Represents a tool argument."""

    model_config = ConfigDict(frozen=True)

    name: str
    value: str


class ToolResult(BaseModel):
    """Result returned by a tool."""

    model_config = ConfigDict(frozen=True)

    success: bool

    output: str = ""
    error: str = ""

    exit_code: int = Field(
        default=0,
        ge=0,
    )


class ToolSelection(BaseModel):
    """Represents the selected tool for execution."""

    model_config = ConfigDict(frozen=True)

    tool_name: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    reason: str


class PermissionDecision(BaseModel):
    """Represents the outcome of a permission check."""

    model_config = ConfigDict(frozen=True)

    allowed: bool
    reason: str


class ValidationResult(BaseModel):
    """Represents the outcome of argument validation."""

    model_config = ConfigDict(frozen=True)

    valid: bool
    reason: str
