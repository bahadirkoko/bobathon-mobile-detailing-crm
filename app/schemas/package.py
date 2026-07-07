"""Package schemas."""

from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel


class PackageCreate(ORMBaseModel):
    """Payload for creating a package."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    base_price_cents: int = Field(ge=0)
    duration_minutes: int = Field(gt=0)
    is_active: bool = True


class PackageUpdate(ORMBaseModel):
    """Payload for updating a package."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    base_price_cents: int | None = Field(default=None, ge=0)
    duration_minutes: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class PackageRead(ORMBaseModel):
    """Serialized package record."""

    id: int
    name: str
    description: str | None = None
    base_price_cents: int
    duration_minutes: int
    is_active: bool
    created_at: datetime
