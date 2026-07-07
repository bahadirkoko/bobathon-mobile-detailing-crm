"""Appointment schemas."""

from datetime import datetime

from pydantic import Field

from app.models.enums import AppointmentPhotoTag, AppointmentStatus
from app.schemas.base import ORMBaseModel
from app.schemas.package import PackageRead


class AppointmentCreate(ORMBaseModel):
    """Payload for creating an appointment."""

    customer_id: int
    vehicle_id: int
    employee_id: int | None = None
    package_id: int
    scheduled_at: datetime
    service_address: str = Field(min_length=1, max_length=500)
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    price_cents: int = Field(ge=0)


class AppointmentUpdate(ORMBaseModel):
    """Payload for updating an appointment."""

    customer_id: int | None = None
    vehicle_id: int | None = None
    employee_id: int | None = None
    package_id: int | None = None
    scheduled_at: datetime | None = None
    service_address: str | None = Field(default=None, min_length=1, max_length=500)
    status: AppointmentStatus | None = None
    price_cents: int | None = Field(default=None, ge=0)
    completed_at: datetime | None = None


class AppointmentPhotoRead(ORMBaseModel):
    """Serialized appointment photo metadata."""

    id: int
    tag: AppointmentPhotoTag
    file_path: str
    created_at: datetime


class AppointmentRead(ORMBaseModel):
    """Serialized appointment record."""

    id: int
    customer_id: int
    vehicle_id: int
    employee_id: int | None = None
    package_id: int
    scheduled_at: datetime
    service_address: str
    status: AppointmentStatus
    price_cents: int
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    package: PackageRead
    photos: list[AppointmentPhotoRead] = []
