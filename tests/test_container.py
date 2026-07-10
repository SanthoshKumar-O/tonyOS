from tony.container import TonyContainer


def test_configuration_is_singleton() -> None:
    container = TonyContainer()

    assert container.configuration is container.configuration


def test_logger_is_singleton() -> None:
    container = TonyContainer()

    assert container.logger is container.logger
