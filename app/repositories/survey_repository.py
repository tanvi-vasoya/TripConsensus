from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.survey_response import SurveyResponse


class SurveyRepository:
    """
    Repository responsible for SurveyResponse database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def create(
        self,
        survey: SurveyResponse,
    ) -> SurveyResponse:
        """
        Create a new survey response.
        """

        try:

            self.db.add(survey)
            self.db.flush()
            self.db.refresh(survey)

            return survey

        except Exception:

            self.db.rollback()
            raise

    def get_by_id(
        self,
        survey_id: UUID,
    ) -> SurveyResponse | None:
        """
        Retrieve a survey response by ID.
        """

        return self.db.get(
            SurveyResponse,
            survey_id,
        )

    def get_all(
        self,
    ) -> list[SurveyResponse]:
        """
        Retrieve all survey responses.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .all()
        )

    def update(
        self,
        survey: SurveyResponse,
    ) -> SurveyResponse:
        """
        Update a survey response.
        """

        try:

            self.db.flush()
            self.db.refresh(survey)

            return survey

        except Exception:

            self.db.rollback()
            raise

    def save(
        self,
        survey: SurveyResponse,
    ) -> SurveyResponse:
        """
        Persist survey changes.
        """

        try:

            self.db.flush()
            self.db.refresh(survey)

            return survey

        except Exception:

            self.db.rollback()
            raise

    def delete(
        self,
        survey_id: UUID,
    ) -> bool:
        """
        Delete a survey response.
        """

        survey = self.get_by_id(
            survey_id,
        )

        if survey is None:
            return False

        try:

            self.db.delete(survey)
            self.db.flush()

            return True

        except Exception:

            self.db.rollback()
            raise

    def exists(
        self,
        survey_id: UUID,
    ) -> bool:
        """
        Check whether a survey response exists.
        """

        return (
            self.db.get(
                SurveyResponse,
                survey_id,
            )
            is not None
        )

    def get_by_participant_id(
        self,
        participant_id: UUID,
    ) -> SurveyResponse | None:
        """
        Retrieve the survey response belonging to a participant.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .filter(
                SurveyResponse.participant_id == participant_id,
            )
            .first()
        )

    def get_by_budget_range(
        self,
        minimum_budget: int,
        maximum_budget: int,
    ) -> list[SurveyResponse]:
        """
        Retrieve surveys within a budget range.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .filter(
                SurveyResponse.budget_per_person >= minimum_budget,
                SurveyResponse.budget_per_person <= maximum_budget,
            )
            .all()
        )

    def get_submitted_between(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[SurveyResponse]:
        """
        Retrieve surveys submitted within a time range.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .filter(
                SurveyResponse.submitted_at >= start_datetime,
                SurveyResponse.submitted_at <= end_datetime,
            )
            .all()
        )

    def search_by_activity(
        self,
        activity: str,
    ) -> list[SurveyResponse]:
        """
        Retrieve surveys containing an activity.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .filter(
                SurveyResponse.preferred_activities.contains(
                    [activity],
                )
            )
            .all()
        )
    
    def get_by_trip_id(
        self,
        trip_id: UUID,  
    ) -> list[SurveyResponse]:
        """
        Retrieve all survey responses for a trip.
        """

        return (
            self.db.query(
                SurveyResponse,
            )
            .join(
                SurveyResponse.participant,
            )
            .filter(
                SurveyResponse.participant.has(
                    trip_id=trip_id,
                )
            )
            .all()
        )