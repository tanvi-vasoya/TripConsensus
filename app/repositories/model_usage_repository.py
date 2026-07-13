from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.model_usage import ModelUsage


class ModelUsageRepository:
    """
    Repository responsible for ModelUsage database operations.

    This class encapsulates all database interactions related to
    the ModelUsage model and provides CRUD operations and
    AI usage-specific database queries.
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
        usage: ModelUsage,
    ) -> ModelUsage:
        """
        Create a new model usage record.
        """

        try:
            self.db.add(usage)
            self.db.commit()
            self.db.refresh(usage)

            return usage

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        usage_id: UUID,
    ) -> ModelUsage | None:
        """
        Retrieve a model usage record by its unique identifier.
        """

        return self.db.get(
            ModelUsage,
            usage_id,
        )

    def get_all(
        self,
    ) -> list[ModelUsage]:
        """
        Retrieve all model usage records.
        """

        return (
            self.db.query(ModelUsage)
            .all()
        )

    def update(
        self,
        usage: ModelUsage,
    ) -> ModelUsage:
        """
        Update an existing model usage record.
        """

        try:
            self.db.commit()
            self.db.refresh(usage)

            return usage

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        usage_id: UUID,
    ) -> bool:
        """
        Delete a model usage record.

        Returns:
            True if the record was deleted.
            False if the record does not exist.
        """

        usage = self.get_by_id(
            usage_id,
        )

        if usage is None:
            return False

        try:
            self.db.delete(usage)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise

    def exists(
        self,
        usage_id: UUID,
    ) -> bool:
        """
        Check whether a model usage record exists.
        """

        return (
            self.db.get(
                ModelUsage,
                usage_id,
            )
            is not None
        )

    def get_by_trip_id(
        self,
        trip_id: UUID,
    ) -> list[ModelUsage]:
        """
        Retrieve all AI model usage records for a trip.
        """

        return (
            self.db.query(ModelUsage)
            .filter(
                ModelUsage.trip_id == trip_id,
            )
            .all()
        )

    def get_by_provider(
        self,
        provider: str,
    ) -> list[ModelUsage]:
        """
        Retrieve all usage records for a provider.
        """

        return (
            self.db.query(ModelUsage)
            .filter(
                ModelUsage.provider == provider,
            )
            .all()
        )

    def get_by_model(
        self,
        model_name: str,
    ) -> list[ModelUsage]:
        """
        Retrieve all usage records for a model.
        """

        return (
            self.db.query(ModelUsage)
            .filter(
                ModelUsage.model_name == model_name,
            )
            .all()
        )

    def get_by_prompt_version(
        self,
        prompt_version: str,
    ) -> list[ModelUsage]:
        """
        Retrieve all usage records for a prompt version.
        """

        return (
            self.db.query(ModelUsage)
            .filter(
                ModelUsage.prompt_version == prompt_version,
            )
            .all()
        )

    def get_total_estimated_cost(
        self,
    ) -> float:
        """
        Calculate the total estimated AI usage cost.
        """

        total = (
            self.db.query(
                func.sum(
                    ModelUsage.estimated_cost,
                )
            )
            .scalar()
        )

        return float(total or 0.0)