"""Ollama provider integrating with Tony's provider infrastructure."""

from __future__ import annotations

from tony.providers.base import Provider
from tony.providers.exceptions import ProviderInitializationError
from tony.providers.ollama.client import OllamaClient
from tony.providers.ollama.exceptions import OllamaError
from tony.providers.ollama.models import OllamaGenerateRequest


class OllamaProvider(Provider):
    def __init__(self, host: str, model: str, timeout: int) -> None:
        super().__init__("ollama")

        self.host = host
        self.model = model
        self.timeout = timeout

        self._client = None

    @property
    def name(self) -> str:
        """Returns the provider's identifying name."""
        return "ollama"

    def initialize(self) -> None:
        """Creates the Ollama client and verifies connectivity.

        Raises:
            ProviderInitializationError: If the Ollama server cannot be
                reached during connectivity verification.
        """
        client = OllamaClient(host=self.host, timeout=self.timeout)

        try:
            client.health()
        except OllamaError as exc:
            raise ProviderInitializationError(
                f"Failed to initialize Ollama provider: {exc}"
            ) from exc

        self._client = client
        self._mark_initialized()

    def shutdown(self) -> None:
        """Closes the Ollama client and marks the provider as shut down."""
        if self._client is not None:
            self._client.close()

        self._client = None
        self._mark_shutdown()

    def health(self) -> bool:
        """Checks whether the Ollama server is currently reachable.

        Returns:
            True if the server responded successfully.

        Raises:
            ProviderInitializationError: If the provider has not been
                initialized.
            OllamaError: If the health check fails.
        """
        if not self.initialized or self._client is None:
            raise ProviderInitializationError("Ollama provider has not been initialized")

        return self._client.health()

    def generate(self, prompt: str) -> str:
        """Generates text from the given prompt using Ollama.

        Args:
            prompt: The prompt text to send to the model.

        Returns:
            The generated text.

        Raises:
            ProviderInitializationError: If the provider has not been
                initialized.
            OllamaError: If the generation request fails.
        """
        if not self.initialized or self._client is None:
            raise ProviderInitializationError("Ollama provider has not been initialized")

        request = OllamaGenerateRequest(model=self.model, prompt=prompt)
        response = self._client.generate(request)

        return response.response
