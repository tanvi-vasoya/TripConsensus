import re
from typing import Any

from app.prompts.registry import registry


class PromptRenderer:
    """
    Renders prompt templates by replacing template variables.
    """

    VARIABLE_PATTERN = re.compile(
        r"\{\{(.*?)\}\}",
    )

    def render(
        self,
        prompt_name: str,
        version: str | None = None,
        **variables: Any,
    ) -> dict:
        """
        Render a prompt template.

        Example:
            renderer.render(
                "destination_recommendation",
                trip=trip,
                participants=participants,
                survey_responses=responses,
            )
        """

        prompt = registry.get(
            prompt_name=prompt_name,
            version=version,
        )

        system_prompt = self._replace_variables(
            prompt["system"],
            variables,
        )

        user_prompt = self._replace_variables(
            prompt["user"],
            variables,
        )

        return {
            "system": system_prompt,
            "user": user_prompt,
            "metadata": prompt.get(
                "metadata",
                {},
            ),
            "output_format": prompt.get(
                "output_format",
            ),
        }

    def _replace_variables(
        self,
        template: str,
        variables: dict[str, Any],
    ) -> str:
        """
        Replace {{variable}} placeholders.
        """

        def format_value(value: Any) -> str:

            if value is None:
                return ""

            # List of SQLAlchemy objects
            if isinstance(value, list):

                lines = []

                for item in value:

                    if hasattr(item, "__dict__"):

                        fields = []

                        for key, val in item.__dict__.items():

                            if key.startswith("_"):
                                continue

                            fields.append(
                                f"{key}: {val}"
                            )

                        lines.append(
                            "\n".join(fields)
                        )

                    else:

                        lines.append(
                            str(item)
                        )

                return "\n\n".join(lines)

            # Single SQLAlchemy object
            if hasattr(value, "__dict__"):

                fields = []

                for key, val in value.__dict__.items():

                    if key.startswith("_"):
                        continue

                    fields.append(
                        f"{key}: {val}"
                    )

                return "\n".join(fields)

            return str(value)

        def replace(match: re.Match) -> str:

            key = match.group(1).strip()

            return format_value(
                variables.get(key)
            )

        return self.VARIABLE_PATTERN.sub(
            replace,
            template,
        )


renderer = PromptRenderer()