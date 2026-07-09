"""Application metadata.

This module is the single source of truth for the application's
identity (name and version). No other module should hardcode these
values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationMetadata:
    """Immutable identity information for the application."""

    name: str
    version: str


APPLICATION_METADATA = ApplicationMetadata(name="Tony", version="0.1.0")
