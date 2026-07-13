from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class VoteCreate(BaseModel):
    """
    Schema for submitting a vote.
    """

    participant_id: UUID = Field(
        description="Participant submitting the vote.",
    )

    recommendation_id: UUID = Field(
        description="Recommendation being ranked.",
    )

    rank: int = Field(
        ...,
        ge=1,
        description="Rank assigned to the recommendation.",
        examples=[1],
    )

class VoteUpdate(BaseModel):
    """
    Schema for updating an existing vote.
    """

    rank: int | None = Field(
        default=None,
        ge=1,
        description="Updated ranking for the recommendation.",
        examples=[2],
    )


class VoteResponse(BaseModel):
    """
    Schema returned when sending vote information.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID = Field(
        description="Unique identifier of the vote.",
    )

    participant_id: UUID = Field(
        description="Participant who submitted the vote.",
    )

    recommendation_id: UUID = Field(
        description="Recommendation being ranked.",
    )

    rank: int = Field(
        description="Ranking assigned by the participant.",
        examples=[1],
    )

    created_at: datetime = Field(
        description="Timestamp when the vote was submitted.",
    )



class VotingResultResponse(BaseModel):
    """
    Schema returned after the Ranked Choice Voting election.
    """

    winner: str | None = Field(
        description="Winning destination. None if the election ends in a tie.",
        examples=["Goa"],
    )