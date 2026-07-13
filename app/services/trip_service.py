from uuid import UUID

from sqlalchemy.orm import Session

from app.models.participant import Participant
from app.models.trip import Trip
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate
from app.services.sms_service import SMSService


class TripService:
    """
    Business service responsible for trip workflows.
    """

    def __init__(
        self,
        db: Session,
        trip_repository: TripRepository,
        participant_repository: ParticipantRepository,
        sms_service: SMSService,
    ) -> None:

        self.db = db
        self.trip_repository = trip_repository
        self.participant_repository = participant_repository
        self.sms_service = sms_service

    def create_trip(
        self,
        trip_data: TripCreate,
    ) -> Trip:
        """
        Create a trip together with its organizer
        and invited participants.
        """

        try:

            # -------------------------
            # Create Trip
            # -------------------------

            trip = Trip(
                title=trip_data.title,
                description=trip_data.description,
            )

            self.db.add(trip)
            self.db.flush()

            # -------------------------
            # Organizer
            # -------------------------

            organizer = Participant(
                trip=trip,
                name=trip_data.organizer.name,
                phone_number=trip_data.organizer.phone_number,
                email=trip_data.organizer.email,
                is_organizer=True,
            )

            self.db.add(organizer)

            # -------------------------
            # Participants
            # -------------------------

            invited_participants = []

            for participant_data in trip_data.participants:

                participant = Participant(
                    trip=trip,
                    name=participant_data.name,
                    phone_number=participant_data.phone_number,
                    email=participant_data.email,
                    is_organizer=False,
                )

                self.db.add(participant)
                invited_participants.append(participant)

            # -------------------------
            # Commit Everything First
            # -------------------------

            self.db.commit()

            self.db.refresh(trip)
            self.db.refresh(organizer)

            for participant in invited_participants:
                self.db.refresh(participant)

            # -------------------------
            # Send SMS
            # (outside transaction)
            # -------------------------

            try:

                self.sms_service.send_trip_invitation(
                    organizer,
                    trip,
                )

                for participant in invited_participants:

                    self.sms_service.send_trip_invitation(
                        participant,
                        trip,
                    )

            except Exception as exc:

                print(
                    f"SMS sending failed: {exc}"
                )

            return trip

        except Exception:

            self.db.rollback()
            raise

    def get_trip(
        self,
        trip_id: UUID,
    ) -> Trip | None:
        """
        Retrieve a trip by ID.
        """

        return self.trip_repository.get_by_id(
            trip_id,
        )

    def get_all_trips(
        self,
    ) -> list[Trip]:
        """
        Retrieve all trips.
        """

        return self.trip_repository.get_all()

    def update_trip(
        self,
        trip: Trip,
    ) -> Trip:
        """
        Update an existing trip.
        """

        return self.trip_repository.update(
            trip,
        )

    def delete_trip(
        self,
        trip_id: UUID,
    ) -> bool:
        """
        Delete a trip.
        """

        return self.trip_repository.delete(
            trip_id,
        )

    def get_organizer(
        self,
        trip_id: UUID,
    ) -> Participant | None:
        """
        Retrieve the organizer.
        """

        participants = self.participant_repository.get_by_trip_id(
            trip_id,
        )

        return next(
            (
                participant
                for participant in participants
                if participant.is_organizer
            ),
            None,
        )

    def get_participants(
        self,
        trip_id: UUID,
    ) -> list[Participant]:
        """
        Retrieve trip participants.
        """

        return self.participant_repository.get_by_trip_id(
            trip_id,
        )