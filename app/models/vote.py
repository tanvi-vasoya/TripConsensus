from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from app.db_types import Timestamp
from app.db_types import UUIDType


class Vote(Base):
    """
    Database model representing a participant's ranked vote.
    """

    __tablename__ = "votes"

    # Primary Key

    id: Mapped[UUID] = mapped_column(
        UUIDType,
        primary_key=True,
        default=uuid4,
    )

    # Foreign Keys

    participant_id: Mapped[UUID] = mapped_column(
        UUIDType,
        ForeignKey("participants.id"),
        nullable=False,
    )

    recommendation_id: Mapped[UUID] = mapped_column(
        UUIDType,
        ForeignKey("recommendations.id"),
        nullable=False,
    )

    # Vote Ranking

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Timestamp

    created_at: Mapped[datetime] = mapped_column(
        Timestamp,
        server_default=func.now(),
    )

    # Relationships

    participant = relationship(
        "Participant",
        back_populates="votes",
    )

    recommendation = relationship(
        "Recommendation",
        back_populates="votes",
    )