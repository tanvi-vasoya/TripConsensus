from app.database import SessionLocal

from app.models.trip import Trip
from app.models.participant import Participant
from app.models.survey_response import SurveyResponse
from app.models.recommendation import Recommendation
from app.models.vote import Vote
from app.models.model_usage import ModelUsage

from app.repositories.trip_repository import TripRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.survey_repository import SurveyRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.vote_repository import VoteRepository
from app.repositories.model_usage_repository import ModelUsageRepository

from datetime import date


def main():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("TESTING REPOSITORIES")
        print("=" * 60)

        trip_repo = TripRepository(db)
        participant_repo = ParticipantRepository(db)
        survey_repo = SurveyRepository(db)
        recommendation_repo = RecommendationRepository(db)
        vote_repo = VoteRepository(db)
        usage_repo = ModelUsageRepository(db)

        # --------------------------------------------------
        # Trip
        # --------------------------------------------------

        trip = Trip(
            title="Repository Test Trip",
            description="Testing repositories",
        )

        trip = trip_repo.create(trip)

        print(f"✅ Trip Created: {trip.id}")

        assert trip_repo.exists(trip.id)
        assert trip_repo.get_by_id(trip.id) is not None
        assert len(trip_repo.search_by_title("Repository")) > 0

        # --------------------------------------------------
        # Participant
        # --------------------------------------------------

        participant = Participant(
            trip_id=trip.id,
            name="Tanvi",
            phone_number="+919999999999",
            email="tanvi@example.com",
            is_organizer=True,
        )

        participant = participant_repo.create(participant)

        print(f"✅ Participant Created: {participant.id}")

        assert participant_repo.exists(participant.id)
        assert participant_repo.get_by_phone_number(
            "+919999999999"
        ) is not None

        # --------------------------------------------------
        # Survey
        # --------------------------------------------------

        survey = SurveyResponse(
            participant_id=participant.id,
            budget_per_person=15000,
            available_from=date(2026, 8, 10),
            available_to=date(2026, 8, 15),
            preferred_climates=["Cold"],
            preferred_activities=["Trekking"],
            food_preferences=["Vegetarian"],
            transport_preferences=["Flight"],
            accommodation_preferences=["Hotel"],
            additional_notes="None",
        )

        survey = survey_repo.create(survey)

        print(f"✅ Survey Created: {survey.id}")

        assert survey_repo.exists(survey.id)
        assert (
            survey_repo.get_by_participant_id(
                participant.id,
            )
            is not None
        )

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        recommendation = Recommendation(
            trip_id=trip.id,
            destination="Manali",
            recommended_start_date=date(2026, 8, 10),
            recommended_end_date=date(2026, 8, 15),
            reason="Matches all preferences.",
            estimated_cost=18000,
            confidence_score=0.95,
            model_provider="Ollama",
            model_name="llama3.2",
            prompt_version="v1",
        )

        recommendation = recommendation_repo.create(
            recommendation,
        )

        print(
            f"✅ Recommendation Created: {recommendation.id}"
        )

        assert recommendation_repo.exists(
            recommendation.id,
        )

        best = recommendation_repo.get_best_recommendation(
            trip.id,
        )

        assert best is not None

        # --------------------------------------------------
        # Vote
        # --------------------------------------------------

        vote = Vote(
            participant_id=participant.id,
            recommendation_id=recommendation.id,
            rank=1,
        )

        vote = vote_repo.create(vote)

        print(f"✅ Vote Created: {vote.id}")

        assert vote_repo.exists(vote.id)

        # --------------------------------------------------
        # Model Usage
        # --------------------------------------------------

        usage = ModelUsage(
            trip_id=trip.id,
            provider="Ollama",
            model_name="llama3.2",
            prompt_version="v1",
            input_tokens=500,
            output_tokens=200,
            response_time=1.2,
            estimated_cost=0.0,
        )

        usage = usage_repo.create(usage)

        print(f"✅ Model Usage Created: {usage.id}")

        assert usage_repo.exists(usage.id)

        total_cost = usage_repo.get_total_estimated_cost()

        print(f"✅ Total Estimated Cost: {total_cost}")

        print()
        print("=" * 60)
        print("🎉 ALL REPOSITORY TESTS PASSED!")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()