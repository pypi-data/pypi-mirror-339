"""Base models for the LightWave ecosystem."""

from datetime import datetime
from typing import Any, ClassVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Base class for all models in the LightWave ecosystem.

    This class extends Pydantic's BaseModel with common functionality
    and configuration settings used across the LightWave ecosystem.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    created_at: datetime | None = Field(
        default=None, description="When this record was created."
    )
    updated_at: datetime | None = Field(
        default=None, description="When this record was last updated."
    )

    def dict_for_api(self) -> dict[str, Any]:
        """Convert the model to a dictionary suitable for API responses."""
        data = self.model_dump(exclude_unset=True)
        # Add any common transformations here
        return data

    @classmethod
    def from_api_response(cls: type["BaseModel"], data: dict[str, Any]) -> "BaseModel":
        """Create a model instance from API response data."""
        # Add any common transformations here
        return cls(**data)
