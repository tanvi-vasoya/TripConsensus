from app.config import settings
from app.gateway.base import BaseProvider
from app.gateway.providers.ollama_provider import OllamaProvider


_PROVIDER_REGISTRY = {
    "ollama": OllamaProvider,
}


def get_provider() -> BaseProvider:
    """
    Return the configured AI provider.
    """

    provider_name = settings.ai_provider.lower()

    provider_class = _PROVIDER_REGISTRY.get(
        provider_name,
    )

    if provider_class is None:

        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )

    return provider_class(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
    )