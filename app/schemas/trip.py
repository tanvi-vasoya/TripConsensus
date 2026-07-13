from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.schemas.participant import ParticipantCreate
from app.schemas.participant import ParticipantResponse


class TripCreate(BaseModel):
    """
    Schema for creating a new trip.

    Rules:
    - 'organizer' contains ONLY the organizer.
    - 'participants' contains everyone EXCEPT the organizer.
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Title of the trip.",
        examples=["Goa College Trip"],
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional description of the trip.",
        examples=["A 4-day trip with college friends."],
    )

    organizer: ParticipantCreate = Field(
        ...,
        description="Organizer of the trip.",
        examples=[
            {
                "name": "Tanvi Vasoya",
                "phone_number": "+919876543210",
                "email": "tanvi@example.com",
            }
        ],
    )

    participants: list[ParticipantCreate] = Field(
        ...,
        min_length=1,
        description="Participants to invite (excluding the organizer).",
        examples=[
            [
                {
                    "name": "Rahul Sharma",
                    "phone_number": "+919876543211",
                    "email": "rahul@example.com",
                },
                {
                    "name": "Priya Patel",
                    "phone_number": "+919876543212",
                    "email": "priya@example.com",
                },
            ]
        ],
    )


class TripUpdate(BaseModel):
    """
    Schema for updating an existing trip.
    """

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Updated title of the trip.",
        examples=["Goa Reunion Trip"],
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Updated description of the trip.",
        examples=["Updated itinerary and travel details."],
    )


class TripResponse(BaseModel):
    """
    Schema returned when sending trip information.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID = Field(
        description="Unique identifier of the trip.",
    )

    title: str = Field(
        description="Trip title.",
        examples=["Goa College Trip"],
    )

    description: str | None = Field(
        default=None,
        description="Trip description.",
    )

    final_start_date: date | None = Field(
        default=None,
        description="Final agreed start date.",
    )

    final_end_date: date | None = Field(
        default=None,
        description="Final agreed end date.",
    )

    status: str = Field(
        description="Current status of the trip.",
        examples=["planning"],
    )

    organizer: ParticipantResponse | None = Field(
        default=None,
        description="Organizer of the trip.",
    )

    participants: list[ParticipantResponse] = Field(
        default_factory=list,
        description="Participants belonging to the trip.",
    )

    created_at: datetime = Field(
        description="Timestamp when the trip was created.",
    )

    updated_at: datetime = Field(
        description="Timestamp when the trip was last updated.",
    )