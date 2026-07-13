from datetime import datetime

from sqlalchemy.orm import Session

from app.models.participant import Participant
from app.models.survey_response import SurveyResponse
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.survey_repository import SurveyRepository
from app.services.sms_service import SMSService
from app.survey.engine import SurveyEngine


class SurveyService:
    """
    Handles the complete survey workflow.
    """

    def __init__(
        self,
        db: Session,
        participant_repository: ParticipantRepository,
        survey_repository: SurveyRepository,
        sms_service: SMSService,
    ) -> None:

        self.db = db
        self.participant_repository = participant_repository
        self.survey_repository = survey_repository
        self.sms_service = sms_service

    def start_survey(
        self,
        participant: Participant,
    ) -> None:
        """
        Start the survey by sending the first question.
        """

        participant.current_question = 1

        self.participant_repository.save(
            participant,
        )

        question = SurveyEngine.get_current_question(
            participant.current_question,
        )

        self.sms_service.client.send_sms(
            to=participant.phone_number,
            body=question.prompt,
        )

    def process_message(
        self,
        phone_number: str,
        message: str,
    ) -> None:
        """
        Process an incoming SMS.
        """

        participant = (
            self.participant_repository.get_by_phone_number(
                phone_number,
            )
        )

        if participant is None:
            return

        question = SurveyEngine.get_current_question(
            participant.current_question,
        )

        if question is None:
            return

        valid = SurveyEngine.validate_answer(
            question.field,
            message,
        )

        if not valid:

            self.sms_service.client.send_sms(
                to=participant.phone_number,
                body=(
                    "Invalid response.\n\n"
                    f"{question.prompt}"
                ),
            )

            return

        self._save_answer(
            participant,
            question.field,
            message,
        )

        participant.current_question += 1

        self.participant_repository.save(
            participant,
        )

        if SurveyEngine.survey_completed(
            participant.current_question,
        ):

            participant.survey_completed = True

            self.participant_repository.save(
                participant,
            )

            self.sms_service.send_thank_you(
                participant,
            )

            return

        next_question = SurveyEngine.get_current_question(
            participant.current_question,
        )

        self.sms_service.client.send_sms(
            to=participant.phone_number,
            body=next_question.prompt,
        )

    def _save_answer(
        self,
        participant: Participant,
        field: str,
        value: str,
    ) -> None:
        """
        Persist a survey answer.
        """

        survey = (
            self.survey_repository.get_by_participant_id(
                participant.id,
            )
        )

        if survey is None:

            survey = SurveyResponse(
                participant_id=participant.id,
                budget_per_person=0,
                available_from=datetime.today().date(),
                available_to=datetime.today().date(),
                preferred_climates=[],
                preferred_activities=[],
                food_preferences=[],
                transport_preferences=[],
                accommodation_preferences=[],
                additional_notes=None,
            )

            self.survey_repository.create(
                survey,
            )

        match field:

            case "budget_per_person":
                survey.budget_per_person = int(value)

            case "available_from":
                survey.available_from = (
                    datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    ).date()
                )

            case "available_to":
                survey.available_to = (
                    datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    ).date()
                )

            case "preferred_climates":
                survey.preferred_climates = [
                    value,
                ]

            case "preferred_activities":
                survey.preferred_activities = [
                    value,
                ]

            case "food_preferences":
                survey.food_preferences = [
                    value,
                ]

            case "transport_preferences":
                survey.transport_preferences = [
                    value,
                ]

            case "accommodation_preferences":
                survey.accommodation_preferences = [
                    value,
                ]

            case "additional_notes":
                survey.additional_notes = value

        self.survey_repository.update(
            survey,
        )