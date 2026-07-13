from datetime import datetime


class SurveyValidator:
    """
    Validates survey answers.
    """

    @staticmethod
    def validate(
        field: str,
        value: str,
    ) -> bool:

        try:

            match field:

                case "budget_per_person":
                    return int(value) > 0

                case "available_from":
                    datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    )
                    return True

                case "available_to":
                    datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    )
                    return True

                case _:
                    return len(value.strip()) > 0

        except Exception:

            return False