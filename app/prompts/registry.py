from app.config import settings
from app.prompts.loader import PromptLoader


class PromptRegistry:
    """
    Registry responsible for loading and caching prompt templates.
    """

    def __init__(
        self,
        loader: PromptLoader | None = None,
    ) -> None:

        self.loader = loader or PromptLoader()
        self._cache: dict[str, dict] = {}

    def get(
        self,
        prompt_name: str,
        version: str | None = None,
    ) -> dict:
        """
        Retrieve a prompt template.

        If no version is supplied, the active version from the
        application settings is used.
        """

        version = version or settings.active_prompt_version

        filename = (
            f"{prompt_name}_{version}.yaml"
        )

        if filename not in self._cache:

            self._cache[filename] = (
                self.loader.load(
                    filename,
                )
            )

        return self._cache[filename]

    def clear_cache(
        self,
    ) -> None:
        """
        Clear the prompt cache.
        """

        self._cache.clear()

    def reload(
        self,
        prompt_name: str,
        version: str | None = None,
    ) -> dict:
        """
        Reload a prompt from disk.
        """

        version = version or settings.active_prompt_version

        filename = (
            f"{prompt_name}_{version}.yaml"
        )

        prompt = self.loader.load(
            filename,
        )

        self._cache[filename] = prompt

        return prompt

    def exists(
        self,
        prompt_name: str,
        version: str | None = None,
    ) -> bool:
        """
        Check whether a prompt exists.
        """

        version = version or settings.active_prompt_version

        filename = (
            f"{prompt_name}_{version}.yaml"
        )

        return self.loader.exists(
            filename,
        )


registry = PromptRegistry()