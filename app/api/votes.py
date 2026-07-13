from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.dependencies import get_voting_service
from app.schemas.vote import VoteCreate
from app.schemas.vote import VoteResponse
from app.services.voting_service import VotingService
from app.schemas.vote import VotingResultResponse

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post(
    "",
    response_model=VoteResponse,
    status_code=201,
)
def create_vote(
    vote: VoteCreate,
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> VoteResponse:
    """
    Submit a ranked vote for a recommendation.
    """

    try:

        created_vote = service.create_vote(
            participant_id=vote.participant_id,
            recommendation_id=vote.recommendation_id,
            rank=vote.rank,
        )

        return VoteResponse.model_validate(
            created_vote,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    

@router.get(
    "/results/{trip_id}",
    response_model=VotingResultResponse,
)
def get_voting_result(
    trip_id: UUID,
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> VotingResultResponse:
    """
    Determine the winning destination using
    Ranked Choice Voting.
    """

    try:

        winner = service.determine_winner(
            trip_id,
        )

        return VotingResultResponse(
            winner=winner,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.get(
    "/{vote_id}",
    response_model=VoteResponse,
)
def get_vote(
    vote_id: UUID,
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> VoteResponse:
    """
    Retrieve a vote by its unique identifier.
    """

    try:

        vote = service.get_vote(
            vote_id,
        )

        return VoteResponse.model_validate(
            vote,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    

@router.get(
    "/recommendation/{recommendation_id}",
    response_model=list[VoteResponse],
)
def get_votes_by_recommendation(
    recommendation_id: UUID,
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> list[VoteResponse]:
    """
    Retrieve all votes for a recommendation.
    """

    try:

        votes = service.get_votes_by_recommendation(
            recommendation_id,
        )

        return [
            VoteResponse.model_validate(
                vote,
            )
            for vote in votes
        ]

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    

@router.delete(
    "/{vote_id}",
    status_code=204,
)
def delete_vote(
    vote_id: UUID,
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> None:
    """
    Delete a vote.
    """

    try:

        service.delete_vote(
            vote_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    

@router.get(
    "/",
    response_model=list[VoteResponse],
)
def get_all_votes(
    service: VotingService = Depends(
        get_voting_service,
    ),
) -> list[VoteResponse]:
    """
    Retrieve all votes.
    """

    votes = service.get_all_votes()

    return [
        VoteResponse.model_validate(
            vote,
        )
        for vote in votes
    ]