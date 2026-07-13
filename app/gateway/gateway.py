from app.gateway.base import BaseProvider
from app.gateway.response import AIResponse
from app.gateway.router import get_provider


class Gateway:
    """
    Unified interface for AI providers.
    """

    def __init__(
        self,
        provider: BaseProvider | None = None,
    ) -> None:

        self.provider = provider or get_provider()

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> AIResponse:
        """
        Generate a response.
        """

        return self.provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )