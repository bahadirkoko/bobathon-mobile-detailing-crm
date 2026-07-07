"""Schema exports for the core CRM entities."""

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentPhotoRead,
    AppointmentRead,
    AppointmentUpdate,
)
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.schemas.package import PackageCreate, PackageRead, PackageUpdate
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate

__all__ = [
    "AppointmentCreate",
    "AppointmentPhotoRead",
    "AppointmentRead",
    "AppointmentUpdate",
    "CustomerCreate",
    "CustomerRead",
    "CustomerUpdate",
    "EmployeeCreate",
    "EmployeeRead",
    "EmployeeUpdate",
    "PackageCreate",
    "PackageRead",
    "PackageUpdate",
    "VehicleCreate",
    "VehicleRead",
    "VehicleUpdate",
]
