"""Persistence protocols."""

from __future__ import annotations

from typing import Protocol


class PersistenceProtocol(Protocol):
    """Protocol for persistence backends."""

    def initialize(self) -> None:
        """Initialize the persistence backend."""
        ...

    def close(self) -> None:
        """Close the persistence backend."""
        ...
