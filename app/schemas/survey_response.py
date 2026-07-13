from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class SurveyResponseCreate(BaseModel):
    """
    Schema for submitting a survey response.
    """

    budget_per_person: int = Field(
        ...,
        gt=0,
        description="Maximum budget per person in INR.",
        examples=[15000],
    )

    available_from: date = Field(
        description="Earliest date the participant is available.",
    )

    available_to: date = Field(
        description="Latest date the participant is available.",
    )

    preferred_climates: list[str] = Field(
        ...,
        min_length=1,
        description="Preferred climates.",
        examples=[["Beach", "Cold"]],
    )

    preferred_activities: list[str] = Field(
        ...,
        min_length=1,
        description="Preferred activities.",
        examples=[["Hiking", "Photography"]],
    )

    food_preferences: list[str] = Field(
        ...,
        min_length=1,
        description="Food preferences.",
        examples=[["Vegetarian"]],
    )

    transport_preferences: list[str] = Field(
        ...,
        min_length=1,
        description="Preferred modes of transport.",
        examples=[["Flight", "Train"]],
    )

    accommodation_preferences: list[str] = Field(
        ...,
        min_length=1,
        description="Preferred accommodation types.",
        examples=[["Hotel", "Resort"]],
    )

    additional_notes: str | None = Field(
        default=None,
        max_length=2000,
        description="Any additional preferences or notes.",
        examples=["Need Wi-Fi and vegetarian meals."],
    )

    @model_validator(mode="after")
    def validate_date_range(self):
        """
        Ensure the available date range is valid.
        """

        if self.available_from > self.available_to:
            raise ValueError(
                "available_from must be before or equal to available_to."
            )

        return self


class SurveyResponseUpdate(BaseModel):
    """
    Schema for updating a survey response.
    """

    budget_per_person: int | None = Field(
        default=None,
        gt=0,
        description="Updated budget per person in INR.",
    )

    available_from: date | None = Field(
        default=None,
        description="Updated available from date.",
    )

    available_to: date | None = Field(
        default=None,
        description="Updated available to date.",
    )

    preferred_climates: list[str] | None = Field(
        default=None,
        min_length=1,
        description="Updated preferred climates.",
    )

    preferred_activities: list[str] | None = Field(
        default=None,
        min_length=1,
        description="Updated preferred activities.",
    )

    food_preferences: list[str] | None = Field(
        default=None,
        min_length=1,
        description="Updated food preferences.",
    )

    transport_preferences: list[str] | None = Field(
        default=None,
        min_length=1,
        description="Updated transport preferences.",
    )

    accommodation_preferences: list[str] | None = Field(
        default=None,
        min_length=1,
        description="Updated accommodation preferences.",
    )

    additional_notes: str | None = Field(
        default=None,
        max_length=2000,
        description="Updated additional notes.",
    )

    @model_validator(mode="after")
    def validate_date_range(self):
        """
        Validate the date range only when both dates are provided.
        """

        if (
            self.available_from is not None
            and self.available_to is not None
            and self.available_from > self.available_to
        ):
            raise ValueError(
                "available_from must be before or equal to available_to."
            )

        return self


class SurveyResponseResponse(BaseModel):
    """
    Schema returned when sending survey response data.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID = Field(
        description="Unique identifier of the survey response.",
    )

    participant_id: UUID = Field(
        description="Participant who submitted the survey.",
    )

    budget_per_person: int = Field(
        description="Budget per person in INR.",
    )

    available_from: date = Field(
        description="Participant's available from date.",
    )

    available_to: date = Field(
        description="Participant's available to date.",
    )

    preferred_climates: list[str] = Field(
        description="Preferred climates.",
    )

    preferred_activities: list[str] = Field(
        description="Preferred activities.",
    )

    food_preferences: list[str] = Field(
        description="Food preferences.",
    )

    transport_preferences: list[str] = Field(
        description="Preferred transport options.",
    )

    accommodation_preferences: list[str] = Field(
        description="Preferred accommodation types.",
    )

    additional_notes: str | None = Field(
        default=None,
        description="Additional notes provided by the participant.",
    )

    submitted_at: datetime = Field(
        description="Timestamp when the survey was submitted.",
    )