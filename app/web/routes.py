from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import Depends

from app.dependencies import get_trip_service

from app.services.trip_service import TripService

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates",
)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
        },
    )


@router.get("/create-trip", response_class=HTMLResponse)
async def create_trip(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="create_trip.html",
        context={
            "request": request,
        },
    )

@router.get(
    "/trips",
    response_class=HTMLResponse,
)
async def trips_page(
    request: Request,
    service: TripService = Depends(
        get_trip_service,
    ),
):

    trips = service.get_all_trips()

    trip_cards = []

    for trip in trips:

        participants = service.get_participants(
            trip.id,
        )

        completed = sum(
            participant.survey_completed
            for participant in participants
        )

        total = len(
            participants,
        )

        trip_cards.append(
            {
                "trip": trip,
                "participants": total,
                "completed": completed,
                "ready_for_vote": (
                    total > 0
                    and completed == total
                ),
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="trips.html",
        context={
            "request": request,
            "trips": trip_cards,
        },
    )

@router.get("/trip/{trip_id}", response_class=HTMLResponse)
async def trip_details(
    request: Request,
    trip_id: str,
    service: TripService = Depends(
        get_trip_service,
    ),
):

    trip = service.get_trip(
        trip_id,
    )

    if trip is None:

        return HTMLResponse(
            "Trip not found.",
            status_code=404,
        )

    participants = service.get_participants(
        trip.id,
    )

    completed_surveys = sum(
        participant.survey_completed
        for participant in participants
    )

    total_participants = len(
        participants,
    )

    return templates.TemplateResponse(
        request=request,
        name="trip_details.html",
        context={
            "request": request,
            "trip": trip,
            "participants": participants,
            "organizer": service.get_organizer(
                trip.id,
            ),
            "completed_surveys": completed_surveys,
            "total_participants": total_participants,
            "can_generate": completed_surveys == total_participants,
        },
    )


@router.get(
    "/trip/{trip_id}/vote",
    response_class=HTMLResponse,
)
async def voting_page(
    request: Request,
    trip_id: str,
):

    return templates.TemplateResponse(
        request=request,
        name="voting.html",
        context={
            "request": request,
            "trip_id": trip_id,
        },
    )


@router.get(
    "/trip/{trip_id}/suggested-trip",
    response_class=HTMLResponse,
)
async def suggested_trip(
    request: Request,
    trip_id: str,
):

    return templates.TemplateResponse(
        request=request,
        name="suggested_trip.html",
        context={
            "request": request,
            "trip_id": trip_id,
        },
    )