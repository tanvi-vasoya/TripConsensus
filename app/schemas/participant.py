from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import EmailStr
from pydantic import StringConstraints


PhoneNumber = Annotated[
    str,
    StringConstraints(
        pattern=r"^\+[1-9]\d{1,14}$",
    ),
]


ParticipantName = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=255,
    ),
]


class ParticipantCreate(BaseModel):
    """
    Schema for adding a participant to a trip.
    """

    name: ParticipantName = Field(
        description="Full name of the participant.",
        examples=["Tanvi Vasoya"],
    )

    phone_number: PhoneNumber = Field(
        description="Participant's phone number in E.164 format.",
        examples=["+919876543210"],
    )

    email: EmailStr | None = Field(
        default=None,
        description="Participant's email address.",
        examples=["tanvi@example.com"],
    )


class ParticipantUpdate(BaseModel):
    """
    Schema for updating participant information.
    """

    name: ParticipantName | None = Field(
        default=None,
        description="Updated participant name.",
        examples=["Tanvi Patel"],
    )

    phone_number: PhoneNumber | None = Field(
        default=None,
        description="Updated participant phone number.",
        examples=["+919999999999"],
    )

    email: EmailStr | None = Field(
        default=None,
        description="Updated participant email address.",
        examples=["tanvi.patel@example.com"],
    )


class ParticipantResponse(BaseModel):
    """
    Schema returned when sending participant information.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID = Field(
        description="Unique identifier of the participant.",
    )

    trip_id: UUID = Field(
        description="Trip to which the participant belongs.",
    )

    name: ParticipantName = Field(
        description="Participant's full name.",
    )

    phone_number: PhoneNumber = Field(
        description="Participant's phone number.",
    )

    email: EmailStr | None = Field(
        default=None,
        description="Participant's email address.",
    )

    survey_completed: bool = Field(
        description="Whether the participant has completed the survey.",
    )

    is_organizer: bool = Field(
        description="Whether the participant is the organizer of the trip.",
    )

    joined_at: datetime = Field(
        description="Timestamp when the participant joined the trip.",
    )