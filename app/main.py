from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.routes import router as web_router

from app.config import settings
from app.database import Base
from app.database import engine

# Import all models BEFORE create_all
from app.models.model_usage import ModelUsage
from app.models.participant import Participant
from app.models.recommendation import Recommendation
from app.models.survey_response import SurveyResponse
from app.models.trip import Trip
from app.models.vote import Vote

# Import routers
from app.api.recommendations import router as recommendation_router
from app.api.sms_webhook import router as sms_router
from app.api.trips import router as trip_router
from app.api.votes import router as vote_router
from app.api.survey import router as survey_router
from app.utils.logging import logger

# Automatically create tables on application startup.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=True,
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


app.include_router(sms_router)
app.include_router(recommendation_router)
app.include_router(vote_router)
app.include_router(survey_router)
app.include_router(web_router)
app.include_router(trip_router,prefix="/api",)


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
