from app.survey.questions import QUESTIONS
from app.survey.questions import SurveyQuestion


class SurveyStateMachine:
    """
    Controls survey progression.
    """

    @staticmethod
    def current_question(
        question_number: int,
    ) -> SurveyQuestion | None:

        for question in QUESTIONS:

            if question.id == question_number:
                return question

        return None

    @staticmethod
    def next_question(
        question_number: int,
    ) -> SurveyQuestion | None:

        return SurveyStateMachine.current_question(
            question_number + 1,
        )

    @staticmethod
    def is_complete(
        question_number: int,
    ) -> bool:

        return question_number > len(
            QUESTIONS,
        )