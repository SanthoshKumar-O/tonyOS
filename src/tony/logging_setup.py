"""Standard-library logging configuration for Tony.

This module is intentionally minimal: it configures the root logger
once, at process startup. No custom handlers, formatters registries,
or third-party logging frameworks are introduced here.
"""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger for the application process.

    Args:
        level: The minimum log level to emit. Defaults to INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
