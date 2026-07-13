from uuid import UUID

from sqlalchemy.orm import Session

from app.models.vote import Vote
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.vote_repository import VoteRepository

from collections import defaultdict

from app.algorithms.ranked_choice import Ballot
from app.algorithms.ranked_choice import RankedChoiceVoting


class VotingService:
    """
    Service responsible for recommendation voting.
    """

    def __init__(
        self,
        db: Session,
        vote_repository: VoteRepository,
        recommendation_repository: RecommendationRepository,
        participant_repository: ParticipantRepository,
    ) -> None:

        self.db = db
        self.vote_repository = vote_repository
        self.recommendation_repository = recommendation_repository
        self.participant_repository = participant_repository

    def create_vote(
        self,
        participant_id: UUID,
        recommendation_id: UUID,
        rank: int,
    ) -> Vote:
        """
        Create a ranked vote.
        """

        participant = self.participant_repository.get_by_id(
            participant_id,
        )

        if participant is None:
            raise ValueError(
                "Participant not found.",
            )

        recommendation = (
            self.recommendation_repository.get_by_id(
                recommendation_id,
            )
        )

        if recommendation is None:
            raise ValueError(
                "Recommendation not found.",
            )

        existing_vote = (
            self.vote_repository.get_by_participant_and_recommendation(
                participant_id,
                recommendation_id,
            )
        )

        if existing_vote is not None:
            raise ValueError(
                "Participant has already voted for this recommendation.",
            )

        vote = Vote(
            participant_id=participant_id,
            recommendation_id=recommendation_id,
            rank=rank,
        )

        try:

            created_vote = self.vote_repository.create(
                vote,
            )

            self.db.commit()

            return created_vote

        except Exception:

            self.db.rollback()

            raise




    def get_vote(
        self,
        vote_id: UUID,
    ) -> Vote:
        """
        Retrieve a vote by its unique identifier.
        """

        vote = self.vote_repository.get_by_id(
            vote_id,
        )

        if vote is None:

            raise ValueError(
                "Vote not found.",
            )

        return vote
    


    def get_votes_by_recommendation(
        self,
        recommendation_id: UUID,
    ) -> list[Vote]:
        """
        Retrieve all votes for a recommendation.
        """

        recommendation = (
            self.recommendation_repository.get_by_id(
                recommendation_id,
            )
        )

        if recommendation is None:

            raise ValueError(
                "Recommendation not found.",
            )

        return self.vote_repository.get_by_recommendation_id(
            recommendation_id,
        )
    

    def delete_vote(
        self,
        vote_id: UUID,
    ) -> bool:
        """
        Delete a vote.
        """

        try:

            deleted = self.vote_repository.delete(
                vote_id,
            )

            if not deleted:

                raise ValueError(
                    "Vote not found.",
                )

            self.db.commit()

            return True

        except Exception:

            self.db.rollback()

            raise


    def get_all_votes(
        self,
    ) -> list[Vote]:
        """
        Retrieve all votes.
        """

        return self.vote_repository.get_all()
    


    def _build_ballots(
        self,
        votes: list[Vote],
    ) -> list[Ballot]:
        """
        Convert database vote rows into ranked ballots.
        """

        grouped_votes: dict[UUID, list[Vote]] = defaultdict(
            list,
        )

        for vote in votes:

            grouped_votes[
                vote.participant_id
            ].append(
                vote,
            )

        ballots: list[Ballot] = []

        for participant_votes in grouped_votes.values():

            participant_votes.sort(
                key=lambda vote: vote.rank,
            )

            preferences: list[str] = []

            for vote in participant_votes:

                recommendation = (
                    self.recommendation_repository.get_by_id(
                        vote.recommendation_id,
                    )
                )

                if recommendation is not None:

                    preferences.append(
                        recommendation.destination,
                    )

            ballots.append(
                Ballot(
                    preferences=preferences,
                )
            )

        return ballots
    




    def determine_winner(
        self,
        trip_id: UUID,
    ) -> str | None:
        """
        Determine the winning destination using
        Ranked Choice Voting.
        """

        recommendations = (
            self.recommendation_repository.get_by_trip_id(
                trip_id,
            )
        )

        if not recommendations:

            raise ValueError(
                "No recommendations found.",
            )

        votes: list[Vote] = []

        for recommendation in recommendations:

            votes.extend(
                self.vote_repository.get_by_recommendation_id(
                    recommendation.id,
                )
            )

        if not votes:

            raise ValueError(
                "No votes found.",
            )

        ballots = self._build_ballots(
            votes,
        )

        algorithm = RankedChoiceVoting(
            ballots,
        )

        return algorithm.run()