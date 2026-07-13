from app.survey.state_machine import SurveyStateMachine
from app.survey.validators import SurveyValidator


class SurveyEngine:
    """
    Core survey engine.
    """

    @staticmethod
    def get_current_question(
        current_question: int,
    ):

        return SurveyStateMachine.current_question(
            current_question,
        )

    @staticmethod
    def get_next_question(
        current_question: int,
    ):

        return SurveyStateMachine.next_question(
            current_question,
        )

    @staticmethod
    def validate_answer(
        field: str,
        answer: str,
    ) -> bool:

        return SurveyValidator.validate(
            field,
            answer,
        )

    @staticmethod
    def survey_completed(
        current_question: int,
    ) -> bool:

        return SurveyStateMachine.is_complete(
            current_question,
        )