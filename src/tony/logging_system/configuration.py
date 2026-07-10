from __future__ import annotations

import logging

from tony.configuration.models import LoggingConfig


def configure_logging(config: LoggingConfig) -> None:
    """Configure Tony's logging system."""

    logging.basicConfig(
        level=getattr(logging, config.level.value),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )