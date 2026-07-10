from __future__ import annotations

from pathlib import Path

from .loader import ConfigurationLoader
from .models import TonyConfiguration


class ConfigurationManager:
    """Coordinates loading and validation."""

    DEFAULT_CONFIG_PATH = Path("config.toml")

    @classmethod
    def load(
        cls,
        path: Path | None = None,
    ) -> TonyConfiguration:
        loader = ConfigurationLoader(path or cls.DEFAULT_CONFIG_PATH)

        raw = loader.load()

        return TonyConfiguration.model_validate(raw)
