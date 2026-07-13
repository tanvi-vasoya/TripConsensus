from dataclasses import dataclass


@dataclass(slots=True)
class AIResponse:
    """
    Standard response returned by every AI provider.
    """

    content: str
    provider: str
    model: str
    latency: float