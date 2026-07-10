from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


class ConfigurationLoader:
    """Loads configuration from TOML and environment variables."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> dict[str, Any]:
        config: dict[str, Any] = {}

        if self._path.exists():
            with self._path.open("rb") as file:
                config = tomllib.load(file)

        self._apply_environment_overrides(config)

        return config

    def _apply_environment_overrides(
        self,
        config: dict[str, Any],
    ) -> None:
        application = config.setdefault("application", {})
        logging = config.setdefault("logging", {})

        if value := os.getenv("TONY_APPLICATION_NAME"):
            application["name"] = value

        if value := os.getenv("TONY_ENVIRONMENT"):
            application["environment"] = value

        if value := os.getenv("TONY_LOG_LEVEL"):
            logging["level"] = value
