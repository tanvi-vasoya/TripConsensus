from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from app.db_types import ShortText
from app.db_types import Timestamp
from app.db_types import UUIDType


class ModelUsage(Base):
    """
    Database model representing AI model usage statistics.
    """

    __tablename__ = "model_usage"

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

    # AI Metadata
    provider: Mapped[str] = mapped_column(
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

    # Usage Statistics
    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    response_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    estimated_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        Timestamp,
        server_default=func.now(),
    )


    # Relationships

    trip = relationship(
        "Trip",
        back_populates="model_usages",
    )