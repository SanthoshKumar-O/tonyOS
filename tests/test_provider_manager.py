from tony.providers import Provider, ProviderManager



class DummyProvider(Provider):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def initialize(self) -> None:
        self._mark_initialized()

    def shutdown(self) -> None:
        self._mark_shutdown()

    def generate(self, prompt: str) -> str:
        return "dummy response"


def test_register_provider() -> None:
    manager = ProviderManager()
    provider = DummyProvider("dummy")

    manager.register(provider)

    assert manager.has("dummy")


def test_get_provider() -> None:
    manager = ProviderManager()
    provider = DummyProvider("dummy")

    manager.register(provider)

    assert manager.get("dummy") is provider


def test_unregister_provider() -> None:
    manager = ProviderManager()
    provider = DummyProvider("dummy")

    manager.register(provider)
    manager.unregister("dummy")

    assert not manager.has("dummy")
