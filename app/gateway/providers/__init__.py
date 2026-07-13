from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class that every AI provider must implement.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the language model.
        """
        raise NotImplementedError