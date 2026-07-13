import json
import re

from app.gateway.response import AIResponse


class RecommendationParser:
    """
    Converts an AI response into recommendation dictionaries.
    """

    def parse(
        self,
        response: AIResponse,
    ) -> list[dict]:
        """
        Parse the AI JSON response.
        """

        content = response.content.strip()

        # -----------------------------------------
        # Extract first JSON object from response
        # -----------------------------------------

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL,
        )

        if match is None:
            raise ValueError(
                "No JSON found in AI response."
            )

        json_text = match.group()

        try:

            data = json.loads(
                json_text,
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "AI returned invalid JSON."
            ) from exc

        recommendations = data.get(
            "recommendations",
        )

        if not isinstance(
            recommendations,
            list,
        ):
            raise ValueError(
                "Missing 'recommendations' list."
            )

        return recommendations


parser = RecommendationParser()