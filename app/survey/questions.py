from dataclasses import dataclass


@dataclass(frozen=True)
class SurveyQuestion:
    """
    Represents a single survey question.
    """

    id: int
    field: str
    prompt: str


QUESTIONS: list[SurveyQuestion] = [
    SurveyQuestion(
        id=1,
        field="budget_per_person",
        prompt="What is your budget per person (INR)?",
    ),
    SurveyQuestion(
        id=2,
        field="available_from",
        prompt="What is your available start date? (YYYY-MM-DD)",
    ),
    SurveyQuestion(
        id=3,
        field="available_to",
        prompt="What is your available end date? (YYYY-MM-DD)",
    ),
    SurveyQuestion(
        id=4,
        field="preferred_climates",
        prompt="Preferred climate? (Beach, Mountains, Snow, Desert)",
    ),
    SurveyQuestion(
        id=5,
        field="preferred_activities",
        prompt="Preferred activities? (Adventure, Trekking, Relaxation, Nightlife)",
    ),
    SurveyQuestion(
        id=6,
        field="food_preferences",
        prompt="Food preferences?",
    ),
    SurveyQuestion(
        id=7,
        field="transport_preferences",
        prompt="Preferred transport?",
    ),
    SurveyQuestion(
        id=8,
        field="accommodation_preferences",
        prompt="Preferred accommodation?",
    ),
    SurveyQuestion(
        id=9,
        field="additional_notes",
        prompt="Any additional notes?",
    ),
]