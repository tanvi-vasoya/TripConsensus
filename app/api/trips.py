from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.dependencies import get_trip_service
from app.schemas.trip import TripCreate
from app.schemas.trip import TripResponse
from app.services.trip_service import TripService


router = APIRouter(
    prefix="/trips",
    tags=["Trips"],
)


def build_trip_response(
    service: TripService,
    trip,
) -> TripResponse:
    """
    Build a TripResponse from a Trip model.
    """

    return TripResponse(
        id=trip.id,
        title=trip.title,
        description=trip.description,
        final_start_date=trip.final_start_date,
        final_end_date=trip.final_end_date,
        status=trip.status.value,
        organizer=service.get_organizer(
            trip.id,
        ),
        participants=service.get_participants(
            trip.id,
        ),
        created_at=trip.created_at,
        updated_at=trip.updated_at,
    )

@router.post(
    "",
    response_model=TripResponse,
    status_code=201,
)
def create_trip(
    trip: TripCreate,
    service: TripService = Depends(
        get_trip_service,
    ),
) -> TripResponse:
    """
    Create a new trip.
    """

    try:

        created_trip = service.create_trip(
            trip,
        )

        return build_trip_response(
            service,
            created_trip,
        )

    except Exception as exc:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[TripResponse],
)
def get_all_trips(
    service: TripService = Depends(
        get_trip_service,
    ),
) -> list[TripResponse]:
    """
    Retrieve all trips.
    """

    return [
        build_trip_response(
            service,
            trip,
        )
        for trip in service.get_all_trips()
    ]


@router.get(
    "/{trip_id}",
    response_model=TripResponse,
)
def get_trip(
    trip_id: UUID,
    service: TripService = Depends(
        get_trip_service,
    ),
) -> TripResponse:
    """
    Retrieve a trip by ID.
    """

    trip = service.get_trip(
        trip_id,
    )

    if trip is None:

        raise HTTPException(
            status_code=404,
            detail="Trip not found.",
        )

    return build_trip_response(
        service,
        trip,
    )


@router.delete(
    "/{trip_id}",
    status_code=204,
)
def delete_trip(
    trip_id: UUID,
    service: TripService = Depends(
        get_trip_service,
    ),
) -> None:
    """
    Delete a trip.
    """

    deleted = service.delete_trip(
        trip_id,
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Trip not found.",
        )