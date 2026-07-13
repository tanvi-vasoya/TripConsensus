from uuid import UUID

from sqlalchemy.orm import Session

from app.models.vote import Vote


class VoteRepository:
    """
    Repository responsible for Vote database operations.

    This class encapsulates all database interactions related to
    the Vote model and provides CRUD operations and
    vote-specific database queries.
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
        vote: Vote,
    ) -> Vote:
        """
        Create a new vote.
        """

        try:
            self.db.add(vote)
            self.db.flush()
            self.db.refresh(vote)

            return vote

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        vote_id: UUID,
    ) -> Vote | None:
        """
        Retrieve a vote by its unique identifier.
        """

        return self.db.get(
            Vote,
            vote_id,
        )

    def get_all(
        self,
    ) -> list[Vote]:
        """
        Retrieve all votes.
        """

        return (
            self.db.query(Vote)
            .all()
        )

    def update(
        self,
        vote: Vote,
    ) -> Vote:
        """
        Update an existing vote.
        """

        try:
            self.db.commit()
            self.db.refresh(vote)

            return vote

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        vote_id: UUID,
    ) -> bool:
        """
        Delete a vote.

        Returns:
            True if the vote was deleted.
            False if the vote does not exist.
        """

        vote = self.get_by_id(
            vote_id,
        )

        if vote is None:
            return False

        try:
            self.db.delete(vote)
            self.db.flush()

            return True

        except Exception:
            self.db.rollback()
            raise

    def exists(
        self,
        vote_id: UUID,
    ) -> bool:
        """
        Check whether a vote exists.
        """

        return (
            self.db.get(
                Vote,
                vote_id,
            )
            is not None
        )

    def get_by_participant_id(
        self,
        participant_id: UUID,
    ) -> list[Vote]:
        """
        Retrieve all votes submitted by a participant.
        """

        return (
            self.db.query(Vote)
            .filter(
                Vote.participant_id == participant_id,
            )
            .all()
        )

    def get_by_recommendation_id(
        self,
        recommendation_id: UUID,
    ) -> list[Vote]:
        """
        Retrieve all votes for a recommendation.
        """

        return (
            self.db.query(Vote)
            .filter(
                Vote.recommendation_id == recommendation_id,
            )
            .all()
        )

    def get_by_participant_and_recommendation(
        self,
        participant_id: UUID,
        recommendation_id: UUID,
    ) -> Vote | None:
        """
        Retrieve a participant's vote for a specific recommendation.
        """

        return (
            self.db.query(Vote)
            .filter(
                Vote.participant_id == participant_id,
                Vote.recommendation_id == recommendation_id,
            )
            .first()
        )

    def get_ranked_votes(
        self,
        recommendation_id: UUID,
    ) -> list[Vote]:
        """
        Retrieve all votes for a recommendation ordered by rank.
        """

        return (
            self.db.query(Vote)
            .filter(
                Vote.recommendation_id == recommendation_id,
            )
            .order_by(
                Vote.rank.asc(),
            )
            .all()
        )