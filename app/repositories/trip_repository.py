from uuid import UUID

from sqlalchemy.orm import Session

from app.models.trip import Trip


class TripRepository:
    """
    Repository responsible for Trip database operations.

    This class encapsulates all database interactions related to
    the Trip model and provides a clean interface for CRUD
    operations and custom database queries.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize the repository with a database session.
        """

        self.db = db

    def create(
        self,
        trip: Trip,
    ) -> Trip:
        """
        Create a new trip.
        """

        try:
            self.db.add(trip)
            self.db.flush()
            self.db.refresh(trip)

            return trip

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        trip_id: UUID,
    ) -> Trip | None:
        """
        Retrieve a trip by its unique identifier.
        """

        return self.db.get(
            Trip,
            trip_id,
        )

    def get_all(
        self,
    ) -> list[Trip]:
        """
        Retrieve all trips.
        """

        return (
            self.db.query(Trip)
            .all()
        )

    def update(
        self,
        trip: Trip,
    ) -> Trip:
        """
        Update an existing trip.
        """

        try:
            self.db.flush()
            self.db.refresh(trip)

            return trip

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        trip_id: UUID,
    ) -> bool:
        """
        Delete a trip.

        Returns:
            True if the trip was deleted.
            False if the trip does not exist.
        """

        trip = self.get_by_id(
            trip_id,
        )

        if trip is None:
            return False

        try:
            self.db.delete(trip)
            self.db.flush()

            return True

        except Exception:
            self.db.rollback()
            raise

    def exists(
        self,
        trip_id: UUID,
    ) -> bool:
        """
        Check whether a trip exists.
        """

        return (
            self.db.get(
                Trip,
                trip_id,
            )
            is not None
        )

    def get_by_status(
        self,
        status: str,
    ) -> list[Trip]:
        """
        Retrieve all trips having the specified status.
        """

        return (
            self.db.query(Trip)
            .filter(Trip.status == status)
            .all()
        )

    def search_by_title(
        self,
        keyword: str,
    ) -> list[Trip]:
        """
        Search trips whose title contains the given keyword.
        """

        return (
            self.db.query(Trip)
            .filter(
                Trip.title.ilike(f"%{keyword}%")
            )
            .all()
        )