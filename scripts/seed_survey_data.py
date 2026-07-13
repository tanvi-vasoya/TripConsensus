import app.models

from datetime import date

from app.database import SessionLocal
from app.models.participant import Participant
from app.models.survey_response import SurveyResponse


def seed() -> None:
    """
    Seed fake survey responses for all participants.
    """

    db = SessionLocal()

    try:

        participants = (
            db.query(Participant)
            .order_by(Participant.name)
            .all()
        )

        if not participants:
            print("❌ No participants found.")
            return

        for participant in participants:

            # Skip if survey already exists
            existing = (
                db.query(SurveyResponse)
                .filter(
                    SurveyResponse.participant_id == participant.id,
                )
                .first()
            )

            if existing:
                print(
                    f"✓ Survey already exists for {participant.name}"
                )
                continue

            if participant.name == "Tanvi Vasoya":

                survey = SurveyResponse(
                    participant_id=participant.id,
                    budget_per_person=7000,
                    available_from=date(2026, 8, 1),
                    available_to=date(2026, 8, 5),
                    preferred_climates=[
                        "Beach",
                        "Warm",
                    ],
                    preferred_activities=[
                        "Adventure",
                        "Nightlife",
                    ],
                    food_preferences=[
                        "Vegetarian",
                    ],
                    transport_preferences=[
                        "Flight",
                    ],
                    accommodation_preferences=[
                        "Hotel",
                    ],
                    additional_notes="Looking for a fun college trip.",
                )

            elif participant.name == "Rahul Sharma":

                survey = SurveyResponse(
                    participant_id=participant.id,
                    budget_per_person=9000,
                    available_from=date(2026, 8, 2),
                    available_to=date(2026, 8, 6),
                    preferred_climates=[
                        "Beach",
                    ],
                    preferred_activities=[
                        "Water Sports",
                        "Party",
                    ],
                    food_preferences=[
                        "Any",
                    ],
                    transport_preferences=[
                        "Train",
                    ],
                    accommodation_preferences=[
                        "Resort",
                    ],
                    additional_notes="Excited for water activities.",
                )

            else:

                survey = SurveyResponse(
                    participant_id=participant.id,
                    budget_per_person=8000,
                    available_from=date(2026, 8, 1),
                    available_to=date(2026, 8, 5),
                    preferred_climates=[
                        "Pleasant",
                    ],
                    preferred_activities=[
                        "Sightseeing",
                        "Photography",
                    ],
                    food_preferences=[
                        "Vegetarian",
                    ],
                    transport_preferences=[
                        "Flight",
                    ],
                    accommodation_preferences=[
                        "Hotel",
                    ],
                    additional_notes="Love peaceful destinations.",
                )

            db.add(survey)

            print(
                f"✅ Added survey for {participant.name}"
            )

        db.commit()

        print("\n🎉 Survey seed completed.")

    except Exception as exc:

        db.rollback()

        print(exc)

    finally:

        db.close()


if __name__ == "__main__":
    seed()