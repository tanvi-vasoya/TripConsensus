from uuid import UUID

from sqlalchemy.orm import Session

from app.models.participant import Participant
from app.models.survey_response import SurveyResponse
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.survey_repository import SurveyRepository
from app.schemas.survey_response import SurveyResponseCreate


class WebSurveyService:
    """
    Handles the web-based survey workflow.
    """

    def __init__(
        self,
        db: Session,
        participant_repository: ParticipantRepository,
        survey_repository: SurveyRepository,
    ) -> None:

        self.db = db
        self.participant_repository = participant_repository
        self.survey_repository = survey_repository

    def get_participant(
        self,
        participant_id: UUID,
    ) -> Participant:
        """
        Retrieve a participant by ID.
        """

        participant = self.participant_repository.get_by_id(
            participant_id,
        )

        if participant is None:
            raise ValueError(
                "Participant not found.",
            )

        return participant

    def submit_survey(
        self,
        participant_id: UUID,
        survey_data: SurveyResponseCreate,
    ) -> Participant:
        """
        Save a completed web survey.
        """

        participant = self.get_participant(
            participant_id,
        )

        survey = SurveyResponse(
            participant_id=participant.id,
            budget_per_person=survey_data.budget_per_person,
            available_from=survey_data.available_from,
            available_to=survey_data.available_to,
            preferred_climates=survey_data.preferred_climates,
            preferred_activities=survey_data.preferred_activities,
            food_preferences=survey_data.food_preferences,
            transport_preferences=survey_data.transport_preferences,
            accommodation_preferences=survey_data.accommodation_preferences,
            additional_notes=survey_data.additional_notes,
        )

        try:

            self.survey_repository.create(
                survey,
            )

            participant.survey_completed = True

            self.participant_repository.save(
                participant,
            )

            self.db.commit()

            return participant

        except Exception:

            self.db.rollback()

            raise