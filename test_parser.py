from app.database import SessionLocal
from app.prompts.renderer import renderer
from app.repositories.trip_repository import TripRepository
from app.repositories.survey_repository import SurveyRepository
from app.gateway.gateway import Gateway
from app.ai.recommendation_parser import parser

TRIP_ID = "d2472cc5-7b9a-4f47-a51b-aad3df12b852"

db = SessionLocal()

trip_repo = TripRepository(db)
survey_repo = SurveyRepository(db)
gateway = Gateway()

trip = trip_repo.get_by_id(TRIP_ID)
survey = survey_repo.get_by_trip_id(TRIP_ID)

prompt = renderer.render(
    "destination_recommendation",
    trip=trip,
    participants=trip.participants,
    survey_responses=survey,
)

system_prompt = "\n\n".join(
    [
        prompt["system"],
        prompt.get("output_format", ""),
    ]
)

response = gateway.generate(
    system_prompt=system_prompt,
    user_prompt=prompt["user"],
)

print("=" * 80)
print("PARSER OUTPUT")
print("=" * 80)

parsed = parser.parse(response)

print(parsed)