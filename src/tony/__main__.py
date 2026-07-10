"""Application entry point for Tony."""

from __future__ import annotations

import time

from tony.configuration import ConfigurationManager
from tony.core.application import TonyApplication
from tony.core.bootstrap import ApplicationBootstrap
from tony.logging_system import configure_logging
from tony.metadata import APPLICATION_METADATA


def main() -> None:
    """Run the Tony application."""
    config = ConfigurationManager.load()
    configure_logging(config.logging)

    print(f"{APPLICATION_METADATA.name} v{APPLICATION_METADATA.version}")

    application = TonyApplication(APPLICATION_METADATA)
    bootstrap = ApplicationBootstrap(application)

    bootstrap.startup()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        bootstrap.shutdown()


if __name__ == "__main__":
    main()
