from app.database import SessionLocal

from app.gateway.gateway import Gateway

from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.survey_repository import SurveyRepository
from app.repositories.trip_repository import TripRepository

from app.services.recommendation_service import RecommendationService


TRIP_ID = "a8d96988-bdc3-474f-8fce-3c712600bc95"


db = SessionLocal()

service = RecommendationService(
    db=db,
    recommendation_repository=RecommendationRepository(db),
    survey_repository=SurveyRepository(db),
    trip_repository=TripRepository(db),
    gateway=Gateway(),
)

try:

    recommendations = service.generate_recommendations(
        TRIP_ID,
    )

    print(recommendations)

except Exception:

    import traceback

    traceback.print_exc()

finally:

    db.close()