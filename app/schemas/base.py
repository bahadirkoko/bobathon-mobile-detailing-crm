"""Shared schema utilities."""

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    """Base model configured for SQLAlchemy object serialization."""

    model_config = ConfigDict(from_attributes=True)
