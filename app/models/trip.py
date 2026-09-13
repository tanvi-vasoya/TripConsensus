#Each model corresponds to a table in your database.
#This model generates the corresponding table in PostgreSQL automatically as the application starts.
from datetime import date
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Date,Enum,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
from app.db_types import LongText
from app.db_types import ShortText
from app.db_types import Timestamp
from app.db_types import UUIDType
from app.models.enums import TripStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.participant import Participant


class Trip(Base):
    """Database model representing a trip."""
    __tablename__ = "trips"

    # Primary Key
    id: Mapped[UUID] = mapped_column(UUIDType,primary_key=True,default=uuid4)
    # Trip Information
    title: Mapped[str] = mapped_column(ShortText,nullable=False)
    #Trip Description
    description: Mapped[str | None] = mapped_column(LongText,nullable=True)
    # Finalized Date
    final_start_date: Mapped[date | None] = mapped_column(Date,nullable=True)
    final_end_date: Mapped[date | None] = mapped_column(Date,nullable=True,)
    # Trip Status
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus),default=TripStatus.PLANNING,nullable=False)
    # Metadata
    created_at: Mapped[datetime] = mapped_column(Timestamp,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(Timestamp,server_default=func.now(),onupdate=func.now())


    # Relationships
    participants = relationship("Participant",back_populates="trip",cascade="all, delete-orphan")
    recommendations = relationship("Recommendation",back_populates="trip",cascade="all, delete-orphan")
    model_usages = relationship("ModelUsage",back_populates="trip",cascade="all, delete-orphan")

