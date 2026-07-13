from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_web_survey_service
from app.schemas.survey_response import SurveyResponseCreate
from app.services.web_survey_service import WebSurveyService

router = APIRouter(
    tags=["Survey"],
)

templates = Jinja2Templates(
    directory="app/templates",
)


@router.get(
    "/survey/{participant_id}",
    response_class=HTMLResponse,
)
def survey_page(
    request: Request,
    participant_id: UUID,
    service: WebSurveyService = Depends(
        get_web_survey_service,
    ),
):

    try:

        participant = service.get_participant(
            participant_id,
        )

        return templates.TemplateResponse(
            request=request,
            name="survey.html",
            context={
                "participant": participant,
            },
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    

@router.post(
    "/survey/{participant_id}",
    response_class=HTMLResponse,
)
def submit_survey(
    request: Request,
    participant_id: UUID,
    budget_per_person: int = Form(...),
    available_from: str = Form(...),
    available_to: str = Form(...),
    preferred_climates: list[str] = Form(...),
    preferred_activities: list[str] = Form(...),
    food_preferences: str = Form(...),
    transport_preferences: list[str] = Form(...),
    accommodation_preferences: list[str] = Form(...),
    additional_notes: str | None = Form(None),
    service: WebSurveyService = Depends(
        get_web_survey_service,
    ),
):
    

    try:

        survey = SurveyResponseCreate(
            budget_per_person=budget_per_person,
            available_from=available_from,
            available_to=available_to,
            preferred_climates=preferred_climates,
            preferred_activities=preferred_activities,
            food_preferences=[food_preferences],
            transport_preferences=transport_preferences,
            accommodation_preferences=accommodation_preferences,
            additional_notes=additional_notes,
        )

        service.submit_survey(
            participant_id=participant_id,
            survey_data=survey,
        )

        return templates.TemplateResponse(
            request=request,
            name="survey_success.html",
            context={},
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )