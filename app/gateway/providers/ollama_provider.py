import time

from ollama import Client

from app.gateway.base import BaseProvider
from app.gateway.response import AIResponse


class OllamaProvider(BaseProvider):
    """
    Ollama implementation.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
    ) -> None:

        self.client = Client(
            host=base_url,
        )

        self.model = model

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> AIResponse:

        start = time.perf_counter()

        response = self.client.chat(
            model=self.model,
            format="json",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )



        print("\n" + "=" * 80)
        print("OLLAMA RESPONSE")
        print("=" * 80)
        print(response.message.content)
        print("=" * 80 + "\n")

        latency = time.perf_counter() - start

        return AIResponse(
            content=response.message.content,
            provider="ollama",
            model=self.model,
            latency=latency,
        )