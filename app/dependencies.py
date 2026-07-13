from fastapi import Depends
from sqlalchemy.orm import Session
from app.gateway.gateway import Gateway

from app.database import get_db

# Repositories
from app.repositories.model_usage_repository import ModelUsageRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.survey_repository import SurveyRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.vote_repository import VoteRepository

# Services
from app.services.recommendation_service import RecommendationService
from app.services.sms_service import SMSService
from app.services.survey_service import SurveyService
from app.services.trip_service import TripService
from app.services.voting_service import VotingService
from app.services.web_survey_service import WebSurveyService

# SMS
from app.sms.twilio_client import TwilioClient


# ==========================================================
# Database Dependency
# ==========================================================


def get_database() -> Session:
    """
    Provide a database session.
    """

    return Depends(get_db)


# ==========================================================
# Repository Dependencies
# ==========================================================


def get_trip_repository(
    db: Session = Depends(get_db),
) -> TripRepository:

    return TripRepository(db)


def get_participant_repository(
    db: Session = Depends(get_db),
) -> ParticipantRepository:

    return ParticipantRepository(db)


def get_survey_repository(
    db: Session = Depends(get_db),
) -> SurveyRepository:

    return SurveyRepository(db)


def get_recommendation_repository(
    db: Session = Depends(get_db),
) -> RecommendationRepository:

    return RecommendationRepository(db)


def get_vote_repository(
    db: Session = Depends(get_db),
) -> VoteRepository:

    return VoteRepository(db)


def get_model_usage_repository(
    db: Session = Depends(get_db),
) -> ModelUsageRepository:

    return ModelUsageRepository(db)



# External Clients



def get_twilio_client() -> TwilioClient:
    """
    Provide the Twilio client.
    """

    return TwilioClient()

def get_gateway() -> Gateway:
    """
    Provide the AI Gateway.
    """

    return Gateway()

# Service Dependencies


def get_sms_service(
    client: TwilioClient = Depends(
        get_twilio_client,
    ),
) -> SMSService:
    """
    Provide the SMS service.
    """

    return SMSService(
        client=client,
    )


def get_trip_service(
    db: Session = Depends(get_db),
    trip_repository: TripRepository = Depends(
        get_trip_repository,
    ),
    participant_repository: ParticipantRepository = Depends(
        get_participant_repository,
    ),
    sms_service: SMSService = Depends(
        get_sms_service,
    ),
) -> TripService:
    """
    Provide the Trip service.
    """

    return TripService(
        db=db,
        trip_repository=trip_repository,
        participant_repository=participant_repository,
        sms_service=sms_service,
    )


def get_survey_service(
    db: Session = Depends(get_db),
    participant_repository: ParticipantRepository = Depends(
        get_participant_repository,
    ),
    survey_repository: SurveyRepository = Depends(
        get_survey_repository,
    ),
    sms_service: SMSService = Depends(
        get_sms_service,
    ),
) -> SurveyService:
    """
    Provide the Survey service.
    """

    return SurveyService(
        db=db,
        participant_repository=participant_repository,
        survey_repository=survey_repository,
        sms_service=sms_service,
    )

def get_web_survey_service(
    db: Session = Depends(get_db),
    participant_repository: ParticipantRepository = Depends(
        get_participant_repository,
    ),
    survey_repository: SurveyRepository = Depends(
        get_survey_repository,
    ),
) -> WebSurveyService:
    """
    Provide the Web Survey service.
    """

    return WebSurveyService(
        db=db,
        participant_repository=participant_repository,
        survey_repository=survey_repository,
    )

def get_recommendation_service(
    db: Session = Depends(get_db),
    recommendation_repository: RecommendationRepository = Depends(
        get_recommendation_repository,
    ),
    survey_repository: SurveyRepository = Depends(
        get_survey_repository,
    ),
    trip_repository: TripRepository = Depends(
        get_trip_repository,
    ),
    gateway: Gateway = Depends(
        get_gateway,
    ),
) -> RecommendationService:
    """
    Provide the Recommendation service.
    """

    return RecommendationService(
        db=db,
        recommendation_repository=recommendation_repository,
        survey_repository=survey_repository,
        trip_repository=trip_repository,
        gateway=gateway,
    )

def get_voting_service(
    db: Session = Depends(get_db),
    vote_repository: VoteRepository = Depends(
        get_vote_repository,
    ),
    recommendation_repository: RecommendationRepository = Depends(
        get_recommendation_repository,
    ),
    participant_repository: ParticipantRepository = Depends(
        get_participant_repository,
    ),
) -> VotingService:
    """
    Provide the Voting service.
    """

    return VotingService(
        db=db,
        vote_repository=vote_repository,
        recommendation_repository=recommendation_repository,
        participant_repository=participant_repository,
    )