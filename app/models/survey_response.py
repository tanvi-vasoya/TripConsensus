from datetime import date
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from app.db_types import LongText
from app.db_types import Timestamp
from app.db_types import UUIDType


class SurveyResponse(Base):
    """
    Database model representing a participant's survey response.
    """

    __tablename__ = "survey_responses"

    # Primary Key
    id: Mapped[UUID] = mapped_column(
        UUIDType,
        primary_key=True,
        default=uuid4,
    )

    # Foreign Key
    participant_id: Mapped[UUID] = mapped_column(
        UUIDType,
        ForeignKey("participants.id"),
        nullable=False,
    )

    # Budget
    budget_per_person: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Availability
    available_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    available_to: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Preferences
    preferred_climates: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    preferred_activities: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    food_preferences: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    transport_preferences: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    accommodation_preferences: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    # Additional Information
    additional_notes: Mapped[str | None] = mapped_column(
        LongText,
        nullable=True,
    )

    # Metadata
    submitted_at: Mapped[datetime] = mapped_column(
        Timestamp,
        server_default=func.now(),
    )

    # Relationships

    participant = relationship(
        "Participant",
        back_populates="survey_response",
    )