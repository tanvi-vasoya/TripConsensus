
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.recommendation_parser import parser
from app.config import settings
from app.gateway.gateway import Gateway
from app.models.recommendation import Recommendation
from app.prompts.renderer import renderer
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.survey_repository import SurveyRepository
from app.repositories.trip_repository import TripRepository
from app.utils.logging import logger


class RecommendationService:
    """
    Business service responsible for AI recommendation generation.
    """

    def __init__(
        self,
        db: Session,
        recommendation_repository: RecommendationRepository,
        survey_repository: SurveyRepository,
        trip_repository: TripRepository,
        gateway: Gateway,
    ) -> None:

        self.db = db
        self.recommendation_repository = recommendation_repository
        self.survey_repository = survey_repository
        self.trip_repository = trip_repository
        self.gateway = gateway

    def generate_recommendations(
        self,
        trip_id: UUID,
    ) -> list[Recommendation]:

        logger.info(f"Generating recommendations for trip {trip_id}")

        trip = self.trip_repository.get_by_id(trip_id)

        if trip is None:
            logger.error("Trip not found")
            raise ValueError("Trip not found.")

        logger.info(f"Trip loaded: {trip.title}")

        survey_responses = self.survey_repository.get_by_trip_id(trip_id)

        if not survey_responses:
            logger.warning("No survey responses found.")
            raise ValueError("No survey responses found for this trip.")

        logger.info(f"Collected {len(survey_responses)} survey responses")

        prompt = renderer.render(
            "destination_recommendation",
            trip=trip,
            participants=trip.participants,
            survey_responses=survey_responses,
        )

        logger.info("Prompt rendered successfully")

        system_prompt = "\n\n".join(
            [
                prompt["system"],
                prompt.get("output_format", ""),
            ]
        )

        logger.info("Sending request to AI gateway...")

        ai_response = self.gateway.generate(
            system_prompt=system_prompt,
            user_prompt=prompt["user"],
        )

        logger.info(
            f"Model Used: {ai_response.provider} / {ai_response.model}"
        )

        parsed_recommendations = parser.parse(ai_response)

        logger.info(
            f"AI generated {len(parsed_recommendations)} recommendations"
        )

        saved_recommendations = []

        try:

            self.recommendation_repository.delete_by_trip_id(trip_id)

            for item in parsed_recommendations:

                logger.info(
                    f"Saving recommendation: {item.get('destination')}"
                )

                recommendation = Recommendation(
                    trip_id=trip.id,
                    destination=item.get("destination"),
                    recommended_start_date=datetime.strptime(
                        item.get("recommended_start_date"),
                        "%Y-%m-%d",
                    ).date(),
                    recommended_end_date=datetime.strptime(
                        item.get("recommended_end_date"),
                        "%Y-%m-%d",
                    ).date(),
                    reason=item.get("reason"),
                    estimated_cost=float(item.get("estimated_cost")),
                    confidence_score=float(item.get("confidence")),
                    model_provider=ai_response.provider,
                    model_name=ai_response.model,
                    prompt_version=settings.active_prompt_version,
                )

                self.recommendation_repository.create(recommendation)
                saved_recommendations.append(recommendation)

            self.db.commit()

            logger.info(
                f"Successfully saved {len(saved_recommendations)} recommendations"
            )

            return saved_recommendations

        except Exception:

            self.db.rollback()

            logger.exception("Recommendation generation failed")

            raise

    def get_recommendations(
        self,
        trip_id: UUID,
    ) -> list[Recommendation]:

        return self.recommendation_repository.get_by_trip_id(
            trip_id,
        )

    def get_best_recommendation(
        self,
        trip_id: UUID,
    ) -> Recommendation | None:

        return self.recommendation_repository.get_best_recommendation(
            trip_id,
        )

    def delete_recommendation(
        self,
        recommendation_id: UUID,
    ) -> bool:

        try:

            deleted = self.recommendation_repository.delete(
                recommendation_id,
            )

            self.db.commit()

            logger.info("Recommendation deleted successfully")

            return deleted

        except Exception:

            self.db.rollback()

            logger.exception("Failed to delete recommendation")

            raise




# from datetime import datetime
# from uuid import UUID

# from sqlalchemy.orm import Session

# from app.ai.recommendation_parser import parser
# from app.config import settings
# from app.gateway.gateway import Gateway
# from app.models.recommendation import Recommendation
# from app.prompts.renderer import renderer
# from app.repositories.recommendation_repository import (
#     RecommendationRepository,
# )
# from app.repositories.survey_repository import (
#     SurveyRepository,
# )
# from app.repositories.trip_repository import (
#     TripRepository,
# )


# class RecommendationService:
#     """
#     Generates AI-powered destination recommendations.
#     """

#     def __init__(
#         self,
#         db: Session,
#         recommendation_repository: RecommendationRepository,
#         survey_repository: SurveyRepository,
#         trip_repository: TripRepository,
#         gateway: Gateway,
#     ) -> None:

#         self.db = db
#         self.recommendation_repository = recommendation_repository
#         self.survey_repository = survey_repository
#         self.trip_repository = trip_repository
#         self.gateway = gateway

#     def generate_recommendations(
#         self,
#         trip_id: UUID,
#     ) -> list[Recommendation]:
#         """
#         Generate recommendations for a trip.
#         """

#         print("=" * 60)
#         print("STEP 1 - Loading Trip")

#         trip = self.trip_repository.get_by_id(
#             trip_id,
#         )

#         if trip is None:
#             raise ValueError("Trip not found.")

#         print("✓ Trip Loaded")

#         print("=" * 60)
#         print("STEP 2 - Loading Survey Responses")

#         surveys = self.survey_repository.get_by_trip_id(
#             trip_id,
#         )

#         print(f"✓ Loaded {len(surveys)} survey responses")

#         print("=" * 60)
#         print("STEP 3 - Rendering Prompt")

#         prompt = renderer.render(
#             "destination_recommendation",
#             trip=trip,
#             participants=trip.participants,
#             survey_responses=surveys,
#         )

#         print("✓ Prompt Rendered")

#         print("=" * 60)
#         print("STEP 4 - Calling Gateway")

#         response = self.gateway.generate(
#             system_prompt=prompt["system"],
#             user_prompt=prompt["user"],
#         )

#         print("✓ Gateway Response Received")
#         print(response)

#         print("=" * 60)
#         print("STEP 5 - Parsing Response")

#         parsed = parser.parse(
#             response,
#         )

#         print("✓ Parsed Successfully")
#         print(parsed)

#         recommendations = []

#         print("=" * 60)
#         print("STEP 6 - Saving Recommendations")

#         try:

#             for item in parsed:

#                 print(f"Saving {item['destination']}")

#                 recommendation = Recommendation(
#                     trip_id=trip.id,
#                     destination=item["destination"],
#                     recommended_start_date=datetime.strptime(
#                         item["recommended_start_date"],
#                         "%Y-%m-%d",
#                     ).date(),
#                     recommended_end_date=datetime.strptime(
#                         item["recommended_end_date"],
#                         "%Y-%m-%d",
#                     ).date(),
#                     reason=item["reason"],
#                     estimated_cost=float(
#                         item["estimated_cost"],
#                     ),
#                     confidence_score=float(
#                         item["confidence"],
#                     ),
#                     model_provider=response.provider,
#                     model_name=response.model,
#                     prompt_version=settings.active_prompt_version,
#                 )

#                 self.recommendation_repository.create(
#                     recommendation,
#                 )

#                 recommendations.append(
#                     recommendation,
#                 )

#             print("=" * 60)
#             print("STEP 7 - Commit")

#             self.db.commit()

#             print("✓ Database Commit Successful")

#             return recommendations

#         except Exception as exc:

#             print("=" * 60)
#             print("❌ ERROR OCCURRED")
#             print(type(exc).__name__)
#             print(exc)

#             self.db.rollback()

#             raise