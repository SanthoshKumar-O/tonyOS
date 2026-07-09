"""Bootstrap manager.

The Bootstrap class is responsible only for driving an Application
instance through its lifecycle in the correct order, and for ensuring
a clean shutdown even if the process is interrupted (e.g. Ctrl+C).

It contains no AI logic, no configuration system, and no dependency
injection container — it is a thin lifecycle coordinator.
"""

from __future__ import annotations

import logging
import time

from tony.core.application import TonyApplication


class ApplicationBootstrap:
    """Coordinates startup and shutdown of an Application."""

    def __init__(self, application: TonyApplication) -> None:
        self._application = application
        self._logger = logging.getLogger("tony.bootstrap")

    @property
    def application(self) -> TonyApplication:
        return self._application

    def startup(self) -> None:
        """Initialize and start the managed application."""
        self._application.initialize()
        self._application.start()

    def shutdown(self) -> None:
        """Stop the managed application."""
        self._application.stop()

    def run(self) -> None:
        """Run the full lifecycle: startup, wait, shutdown.

        Blocks until interrupted (e.g. Ctrl+C), then shuts down
        cleanly. This is the entry point used by the CLI.
        """
        self.startup()
        try:
            self._wait_until_interrupted()
        finally:
            self.shutdown()

    def _wait_until_interrupted(self) -> None:
        """Block the current thread until a KeyboardInterrupt occurs."""
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            self._logger.info("Interrupt received.")
