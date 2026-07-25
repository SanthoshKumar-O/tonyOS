"""Protocols for Tony's tools."""

from __future__ import annotations

from typing import Protocol

from tony.tools.models import (
    PermissionDecision,
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
    ToolSelection,
    ValidationResult,
)


class ToolProtocol(Protocol):
    """Represents an executable tool."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return the tool metadata."""
        ...

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the tool."""
        ...


class ToolRegistryProtocol(Protocol):
    """Stores and retrieves tools."""

    def register(
        self,
        tool: ToolProtocol,
    ) -> None:
        """Register a tool."""
        ...

    def unregister(
        self,
        name: str,
    ) -> None:
        """Remove a registered tool."""
        ...

    def get(
        self,
        name: str,
    ) -> ToolProtocol:
        """Return a registered tool."""
        ...

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether a tool is registered."""
        ...

    def tools(
        self,
    ) -> list[ToolProtocol]:
        """Return all registered tools."""
        ...


class ToolDiscoveryProtocol(Protocol):
    """Discovers an appropriate tool for execution."""

    def discover(
        self,
        capability: ToolCapability,
    ) -> ToolSelection:
        """Select a tool matching the requested capability."""
        ...


class PermissionEngineProtocol(Protocol):
    """Determines whether a selected tool may execute."""

    def check(
        self,
        selection: ToolSelection,
    ) -> PermissionDecision:
        """Check whether the selected tool is permitted."""
        ...


class ArgumentValidatorProtocol(Protocol):
    """Validates tool arguments."""

    def validate(
        self,
        arguments: list[ToolArgument],
    ) -> ValidationResult:
        """Validate tool arguments."""
        ...


class ToolDispatcherProtocol(Protocol):
    """Dispatches tool execution."""

    def dispatch(
        self,
        selection: ToolSelection,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the selected tool."""
        ...
