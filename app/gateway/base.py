from abc import ABC
from abc import abstractmethod

from app.gateway.response import AIResponse


class BaseProvider(ABC):
    """
    Base interface implemented by every AI provider.
    """

    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> AIResponse:
        """
        Generate a response.
        """
        raise NotImplementedError