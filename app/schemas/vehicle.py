"""Vehicle schemas."""

from pydantic import Field

from app.schemas.base import ORMBaseModel


class VehicleCreate(ORMBaseModel):
    """Payload for creating a vehicle."""

    customer_id: int
    make: str = Field(min_length=1, max_length=255)
    model: str = Field(min_length=1, max_length=255)
    year: int | None = Field(default=None, ge=1900, le=2100)
    color: str | None = Field(default=None, max_length=255)
    vehicle_size: str = Field(min_length=1, max_length=100)
    notes: str | None = Field(default=None, max_length=500)


class VehicleUpdate(ORMBaseModel):
    """Payload for updating a vehicle."""

    customer_id: int | None = None
    make: str | None = Field(default=None, min_length=1, max_length=255)
    model: str | None = Field(default=None, min_length=1, max_length=255)
    year: int | None = Field(default=None, ge=1900, le=2100)
    color: str | None = Field(default=None, max_length=255)
    vehicle_size: str | None = Field(default=None, min_length=1, max_length=100)
    notes: str | None = Field(default=None, max_length=500)


class VehicleRead(ORMBaseModel):
    """Serialized vehicle record."""

    id: int
    customer_id: int
    make: str
    model: str
    year: int | None = None
    color: str | None = None
    vehicle_size: str
    notes: str | None = None
