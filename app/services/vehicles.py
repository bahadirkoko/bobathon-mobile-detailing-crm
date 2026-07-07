"""Vehicle service functions."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.services.customers import CustomerService
from app.services.exceptions import NotFoundError


class VehicleService:
    """Business logic for vehicle records."""

    def __init__(self, customer_service: CustomerService | None = None) -> None:
        """Initialize vehicle dependencies."""
        self.customer_service = customer_service or CustomerService()

    def list_vehicles(self, session: Session) -> list[Vehicle]:
        """Return all vehicles ordered by newest first."""
        statement: Select[tuple[Vehicle]] = select(Vehicle).order_by(Vehicle.id.desc())
        return list(session.scalars(statement))

    def get_vehicle(self, session: Session, vehicle_id: int) -> Vehicle:
        """Return a vehicle by identifier."""
        vehicle = session.get(Vehicle, vehicle_id)
        if vehicle is None:
            raise NotFoundError(f"Vehicle {vehicle_id} was not found.")
        return vehicle

    def create_vehicle(self, session: Session, payload: VehicleCreate) -> Vehicle:
        """Create and persist a vehicle."""
        self.customer_service.get_customer(session, payload.customer_id)
        vehicle = Vehicle(**payload.model_dump())
        session.add(vehicle)
        session.commit()
        session.refresh(vehicle)
        return vehicle

    def update_vehicle(self, session: Session, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
        """Update an existing vehicle."""
        vehicle = self.get_vehicle(session, vehicle_id)
        data = payload.model_dump(exclude_unset=True)
        customer_id = data.get("customer_id")
        if customer_id is not None:
            self.customer_service.get_customer(session, customer_id)
        for field, value in data.items():
            setattr(vehicle, field, value)
        session.commit()
        session.refresh(vehicle)
        return vehicle
