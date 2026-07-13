from app.database import Base
from app.database import engine

# Import every model
from app.models.trip import Trip
from app.models.participant import Participant
from app.models.survey_response import SurveyResponse
from app.models.recommendation import Recommendation
from app.models.vote import Vote
from app.models.model_usage import ModelUsage


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")