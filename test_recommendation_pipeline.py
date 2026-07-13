from app.database import SessionLocal
from app.prompts.renderer import renderer
from app.repositories.trip_repository import TripRepository
from app.repositories.survey_repository import SurveyRepository
from app.gateway.gateway import Gateway

TRIP_ID = "d2472cc5-7b9a-4f47-a51b-aad3df12b852"

db = SessionLocal()

trip_repository = TripRepository(db)
survey_repository = SurveyRepository(db)
gateway = Gateway()

trip = trip_repository.get_by_id(TRIP_ID)

survey_responses = survey_repository.get_by_trip_id(
    trip.id,
)

prompt = renderer.render(
    "destination_recommendation",
    trip=trip,
    participants=trip.participants,
    survey_responses=survey_responses,
)

system_prompt = "\n\n".join(
    [
        prompt["system"],
        prompt.get("output_format", ""),
    ]
)

print("=" * 80)
print("SYSTEM PROMPT")
print("=" * 80)
print(system_prompt)

print("\n" + "=" * 80)
print("USER PROMPT")
print("=" * 80)
print(prompt["user"])

response = gateway.generate(
    system_prompt=system_prompt,
    user_prompt=prompt["user"],
)

print("\n" + "=" * 80)
print("RAW AI RESPONSE")
print("=" * 80)
print(response.content)

db.close()