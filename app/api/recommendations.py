from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
import traceback
from app.dependencies import get_recommendation_service
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "/{trip_id}/generate",
    response_model=list[RecommendationResponse],
    status_code=201,
)
def generate_recommendations(
    trip_id: UUID,
    service: RecommendationService = Depends(
        get_recommendation_service,
    ),
) -> list[RecommendationResponse]:
    
    print("API HIT: generate_recommendations")

    try:

        recommendations = service.generate_recommendations(
            trip_id,
        )

        return [
            RecommendationResponse.model_validate(
                recommendation,
            )
            for recommendation in recommendations
        ]

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        print("=" * 80)
        print("RECOMMENDATION ERROR")
        print("=" * 80)
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
    

@router.get(
    "/{trip_id}",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    trip_id: UUID,
    service: RecommendationService = Depends(
        get_recommendation_service,
    ),
) -> list[RecommendationResponse]:
    """
    Retrieve all recommendations for a trip.
    """

    recommendations = service.get_recommendations(
        trip_id,
    )

    return [
        RecommendationResponse.model_validate(
            recommendation,
        )
        for recommendation in recommendations
    ]
