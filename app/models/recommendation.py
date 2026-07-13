from datetime import date
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from app.db_types import LongText
from app.db_types import ShortText
from app.db_types import Timestamp
from app.db_types import UUIDType


class Recommendation(Base):
    """
    Database model representing an AI-generated trip recommendation.
    """

    __tablename__ = "recommendations"

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

    # AI Recommendation
    destination: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    recommended_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    recommended_end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        LongText,
        nullable=False,
    )

    estimated_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # AI Metadata
    model_provider: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    prompt_version: Mapped[str] = mapped_column(
        ShortText,
        nullable=False,
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        Timestamp,
        server_default=func.now(),
    )


    trip = relationship(
        "Trip",
        back_populates="recommendations",
    )



    votes = relationship(
        "Vote",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )