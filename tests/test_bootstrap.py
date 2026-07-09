from __future__ import annotations

from tony.core.application import ApplicationState, TonyApplication
from tony.core.bootstrap import ApplicationBootstrap
from tony.metadata import ApplicationMetadata


def _make_bootstrap() -> ApplicationBootstrap:
    metadata = ApplicationMetadata(name="TestApp", version="0.0.1")
    application = TonyApplication(metadata=metadata)
    return ApplicationBootstrap(application=application)


def test_startup_initializes_and_starts_application() -> None:
    bootstrap = _make_bootstrap()
    bootstrap.startup()
    assert bootstrap.application.state == ApplicationState.RUNNING


def test_shutdown_stops_application() -> None:
    bootstrap = _make_bootstrap()
    bootstrap.startup()
    bootstrap.shutdown()
    assert bootstrap.application.state == ApplicationState.STOPPED


def test_bootstrap_exposes_the_application_it_manages() -> None:
    metadata = ApplicationMetadata(name="TestApp", version="0.0.1")
    application = TonyApplication(metadata=metadata)
    bootstrap = ApplicationBootstrap(application=application)
    assert bootstrap.application is application
