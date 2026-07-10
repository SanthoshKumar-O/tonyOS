from tony.logging_system import get_logger


def test_get_logger_returns_logger() -> None:
    logger = get_logger(__name__)

    assert logger.name == __name__
