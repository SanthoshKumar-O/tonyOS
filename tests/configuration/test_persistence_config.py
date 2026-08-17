from __future__ import annotations

from pathlib import Path

from tony.configuration import ConfigurationManager


def test_persistence_configuration_is_loaded() -> None:
    configuration = ConfigurationManager.load()

    assert configuration.persistence.database_path == Path("data/tony.db")
