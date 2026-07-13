from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from app.db_types import ShortText
from app.db_types import Timestamp
from app.db_types import UUIDType


class Participant(Base):
    """
    Database model representing a participant in a trip.
    """

    __tablename__ = "participants"

    # Primary Key

    id: Mapped[UUID] = mapped_column(
        UUIDType,
        primary_key=True,
        default=uuid4,
    )

    # Foreign Key

    trip_id: Mapped[UUID] = mapped_column(
        UUIDType,
        ForeignKey("trips.id"),
        nullable=False,
    )

    # Participant Information

    name: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        ShortText,
        nullable=True,
    )

    # Trip Metadata

    survey_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_organizer: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Timestamp

    joined_at: Mapped[datetime] = mapped_column(
        Timestamp,
        server_default=func.now(),
    )

    # Relationships

    trip = relationship(
        "Trip",
        back_populates="participants",
    )

    survey_response = relationship(
        "SurveyResponse",
        back_populates="participant",
        uselist=False,
    )

    votes = relationship(
        "Vote",
        back_populates="participant",
        cascade="all, delete-orphan",
    )


    # Survey State

    current_question: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )