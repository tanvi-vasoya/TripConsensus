from pathlib import Path

import yaml

from app.config import settings


class PromptLoader:
    """
    Loads prompt templates from YAML files.
    """

    def __init__(
        self,
        prompt_directory: str | None = None,
    ) -> None:

        self.prompt_directory = Path(
            prompt_directory or settings.prompt_directory,
        )

    def load(
        self,
        filename: str,
    ) -> dict:
        """
        Load a prompt template.

        Example:
            loader.load("destination_recommendation_v1.yaml")
        """

        file_path = self.prompt_directory / filename

        if not file_path.exists():

            raise FileNotFoundError(
                f"Prompt template not found: {file_path}"
            )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = yaml.safe_load(
                file,
            )

        if not isinstance(
            data,
            dict,
        ):

            raise ValueError(
                "Prompt template must be a YAML object."
            )

        return data

    def exists(
        self,
        filename: str,
    ) -> bool:
        """
        Check whether a prompt exists.
        """

        return (
            self.prompt_directory / filename
        ).exists()