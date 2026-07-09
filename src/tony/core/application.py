"""Application lifecycle.

Defines the Application class, which owns exactly one responsibility:
tracking and transitioning its own lifecycle state through
initialize() -> start() -> stop().

The Application knows nothing about planning, memory, tools, or any
other higher-level concern. Those belong to future modules.
"""

from __future__ import annotations

import logging
from enum import Enum, auto

from tony.metadata import ApplicationMetadata


class ApplicationState(Enum):
    """The lifecycle states an Application can be in."""

    CREATED = auto()
    INITIALIZED = auto()
    RUNNING = auto()
    STOPPED = auto()


class InvalidApplicationStateError(RuntimeError):
    """Raised when a lifecycle method is called from an invalid state."""


class TonyApplication:
    """Represents the core lifecycle of the Tony application."""

    def __init__(self, metadata: ApplicationMetadata) -> None:
        self._metadata = metadata
        self._state = ApplicationState.CREATED
        self._logger = logging.getLogger("tony.application")

    @property
    def metadata(self) -> ApplicationMetadata:
        return self._metadata

    @property
    def state(self) -> ApplicationState:
        return self._state

    def initialize(self) -> None:
        """Transition the application from CREATED to INITIALIZED."""
        if self._state != ApplicationState.CREATED:
            raise InvalidApplicationStateError(
                f"initialize() requires state CREATED, current state is {self._state.name}"
            )
        self._logger.info("Initializing application...")
        self._state = ApplicationState.INITIALIZED
        self._logger.info("Application initialized.")

    def start(self) -> None:
        """Transition the application from INITIALIZED to RUNNING."""
        if self._state != ApplicationState.INITIALIZED:
            raise InvalidApplicationStateError(
                f"start() requires state INITIALIZED, current state is {self._state.name}"
            )
        self._logger.info("Starting %s...", self._metadata.name)
        self._state = ApplicationState.RUNNING
        self._logger.info("%s is running.", self._metadata.name)

    def stop(self) -> None:
        """Transition the application from RUNNING to STOPPED."""
        if self._state != ApplicationState.RUNNING:
            raise InvalidApplicationStateError(
                f"stop() requires state RUNNING, current state is {self._state.name}"
            )
        self._logger.info("Stopping %s...", self._metadata.name)
        self._state = ApplicationState.STOPPED
        self._logger.info("Shutdown complete.")
