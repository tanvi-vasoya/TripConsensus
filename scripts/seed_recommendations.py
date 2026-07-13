import app.models

from datetime import date

from app.database import SessionLocal
from app.models.recommendation import Recommendation
from app.models.trip import Trip


def seed() -> None:
    """
    Seed fake AI recommendations.
    """

    db = SessionLocal()

    try:

        trip = (
            db.query(Trip)
            .first()
        )

        if trip is None:

            print("❌ No trips found.")

            return

        existing = (
            db.query(Recommendation)
            .filter(
                Recommendation.trip_id == trip.id,
            )
            .count()
        )

        if existing > 0:

            print("✓ Recommendations already exist.")

            return

        recommendations = [

            Recommendation(
                trip_id=trip.id,
                destination="Goa",
                recommended_start_date=date(2026, 8, 1),
                recommended_end_date=date(2026, 8, 5),
                reason="Beautiful beaches, nightlife and affordable budget.",
                estimated_cost=7500,
                confidence_score=0.94,
                model_provider="seed",
                model_name="manual",
                prompt_version="v1",
            ),

            Recommendation(
                trip_id=trip.id,
                destination="Manali",
                recommended_start_date=date(2026, 8, 2),
                recommended_end_date=date(2026, 8, 6),
                reason="Mountains, adventure sports and cool weather.",
                estimated_cost=8500,
                confidence_score=0.89,
                model_provider="seed",
                model_name="manual",
                prompt_version="v1",
            ),

            Recommendation(
                trip_id=trip.id,
                destination="Udaipur",
                recommended_start_date=date(2026, 8, 1),
                recommended_end_date=date(2026, 8, 5),
                reason="Palaces, lakes and rich cultural heritage.",
                estimated_cost=7000,
                confidence_score=0.87,
                model_provider="seed",
                model_name="manual",
                prompt_version="v1",
            ),
        ]

        db.add_all(
            recommendations,
        )

        db.commit()

        print("🎉 Seeded 3 recommendations.")

    except Exception as exc:

        db.rollback()

        print(exc)

    finally:

        db.close()


if __name__ == "__main__":
    seed()