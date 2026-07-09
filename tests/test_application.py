from __future__ import annotations

import pytest

from src.tony.metadata import ApplicationMetadata
from tony.core.application import (
    ApplicationState,
    InvalidApplicationStateError,
    TonyApplication,
)


@pytest.fixture
def metadata() -> ApplicationMetadata:
    return ApplicationMetadata(name="TestApp", version="0.0.1")


def test_application_starts_in_created_state(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    assert application.state == ApplicationState.CREATED


def test_initialize_transitions_to_initialized(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    application.initialize()
    assert application.state == ApplicationState.INITIALIZED


def test_initialize_twice_raises(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    application.initialize()
    with pytest.raises(InvalidApplicationStateError):
        application.initialize()


def test_start_requires_initialized_state(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    with pytest.raises(InvalidApplicationStateError):
        application.start()


def test_start_transitions_to_running(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    application.initialize()
    application.start()
    assert application.state == ApplicationState.RUNNING


def test_stop_requires_running_state(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    application.initialize()
    with pytest.raises(InvalidApplicationStateError):
        application.stop()


def test_stop_transitions_to_stopped(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    application.initialize()
    application.start()
    application.stop()
    assert application.state == ApplicationState.STOPPED


def test_full_lifecycle_order(metadata: ApplicationMetadata) -> None:
    application = TonyApplication(metadata=metadata)
    assert application.state == ApplicationState.CREATED

    application.initialize()
    assert application.state == ApplicationState.INITIALIZED

    application.start()
    assert application.state == ApplicationState.RUNNING

    application.stop()
    assert application.state == ApplicationState.STOPPED
