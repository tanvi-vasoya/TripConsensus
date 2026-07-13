from uuid import UUID

from sqlalchemy.orm import Session

from app.models.participant import Participant


class ParticipantRepository:
    """
    Repository responsible for Participant database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def create(
        self,
        participant: Participant,
    ) -> Participant:
        """
        Create a participant.
        """

        try:

            self.db.add(participant)
            self.db.flush()
            self.db.refresh(participant)

            return participant

        except Exception:

            self.db.rollback()
            raise

    def get_by_id(
        self,
        participant_id: UUID,
    ) -> Participant | None:
        """
        Retrieve a participant by ID.
        """

        return self.db.get(
            Participant,
            participant_id,
        )

    def get_all(
        self,
    ) -> list[Participant]:
        """
        Retrieve all participants.
        """

        return (
            self.db.query(Participant)
            .all()
        )

    def update(
        self,
        participant: Participant,
    ) -> Participant:
        """
        Update a participant.
        """

        try:

            self.db.flush()
            self.db.refresh(participant)

            return participant

        except Exception:

            self.db.rollback()
            raise

    def save(
        self,
        participant: Participant,
    ) -> Participant:
        """
        Persist participant changes.
        """

        try:

            self.db.flush()
            self.db.refresh(participant)

            return participant

        except Exception:

            self.db.rollback()
            raise

    def delete(
        self,
        participant_id: UUID,
    ) -> bool:
        """
        Delete a participant.
        """

        participant = self.get_by_id(
            participant_id,
        )

        if participant is None:
            return False

        try:

            self.db.delete(participant)
            self.db.flush()

            return True

        except Exception:

            self.db.rollback()
            raise

    def exists(
        self,
        participant_id: UUID,
    ) -> bool:
        """
        Check whether a participant exists.
        """

        return (
            self.db.get(
                Participant,
                participant_id,
            )
            is not None
        )

    def get_by_trip_id(
        self,
        trip_id: UUID,
    ) -> list[Participant]:
        """
        Retrieve all participants belonging to a trip.
        """

        return (
            self.db.query(Participant)
            .filter(
                Participant.trip_id == trip_id,
            )
            .all()
        )

    def get_organizers(
        self,
        trip_id: UUID,
    ) -> list[Participant]:
        """
        Retrieve organizers of a trip.
        """

        return (
            self.db.query(Participant)
            .filter(
                Participant.trip_id == trip_id,
                Participant.is_organizer.is_(True),
            )
            .all()
        )

    def get_by_phone_number(
        self,
        phone_number: str,
    ) -> Participant | None:
        """
        Retrieve a participant by phone number.
        """

        return (
            self.db.query(Participant)
            .filter(
                Participant.phone_number == phone_number,
            )
            .first()
        )

    def search_by_name(
        self,
        keyword: str,
    ) -> list[Participant]:
        """
        Search participants by name.
        """

        return (
            self.db.query(Participant)
            .filter(
                Participant.name.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )