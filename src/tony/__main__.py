"""Application entry point for Tony."""

from __future__ import annotations

import time

from tony.container import TonyContainer
from tony.core.application import TonyApplication
from tony.core.bootstrap import ApplicationBootstrap
from tony.logging_system import configure_logging
from tony.metadata import APPLICATION_METADATA
from tony.providers.ollama import OllamaProvider


def main() -> None:
    """Run the Tony application."""
    container = TonyContainer()
    configure_logging(container.configuration.logging)
    print(f"{APPLICATION_METADATA.name} v{APPLICATION_METADATA.version}")

    application = TonyApplication(APPLICATION_METADATA)
    bootstrap = ApplicationBootstrap(application)

    bootstrap.startup()
    provider = OllamaProvider(
        host=container.configuration.ollama.host,
        model=container.configuration.ollama.model,
        timeout=container.configuration.ollama.timeout,
    )

    provider.initialize()
    print("Provider initialized")

    try:
        print("About to generate...")
        response = provider.generate("Reply with exactly three words.")
        print("Generate returned")
        print(response)
    finally:
        print("Shutting down provider")
        provider.shutdown()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        bootstrap.shutdown()


if __name__ == "__main__":
    main()
