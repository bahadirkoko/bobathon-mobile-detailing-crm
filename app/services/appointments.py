"""Appointment service functions."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models.appointment import Appointment, AppointmentPhoto
from app.models.enums import AppointmentPhotoTag, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.customers import CustomerService
from app.services.employees import EmployeeService
from app.services.exceptions import NotFoundError, ValidationError
from app.services.storage import AppointmentPhotoStorageService
from app.services.vehicles import VehicleService


class AppointmentService:
    """Business logic for appointment records."""

    def __init__(
        self,
        customer_service: CustomerService | None = None,
        employee_service: EmployeeService | None = None,
        vehicle_service: VehicleService | None = None,
        photo_storage: AppointmentPhotoStorageService | None = None,
    ) -> None:
        """Initialize service dependencies."""
        self.customer_service = customer_service or CustomerService()
        self.employee_service = employee_service or EmployeeService()
        self.vehicle_service = vehicle_service or VehicleService(self.customer_service)
        self.photo_storage = photo_storage or AppointmentPhotoStorageService()

    def list_appointments(self, session: Session) -> list[Appointment]:
        """Return all appointments ordered by newest first."""
        statement: Select[tuple[Appointment]] = (
            select(Appointment)
            .options(
                selectinload(Appointment.photos),
                selectinload(Appointment.customer),
                selectinload(Appointment.vehicle),
                selectinload(Appointment.employee),
            )
            .order_by(Appointment.scheduled_at.desc())
        )
        return list(session.scalars(statement))

    def get_appointment(self, session: Session, appointment_id: int) -> Appointment:
        """Return an appointment by identifier."""
        statement = (
            select(Appointment)
            .options(
                selectinload(Appointment.photos),
                selectinload(Appointment.customer),
                selectinload(Appointment.vehicle),
                selectinload(Appointment.employee),
            )
            .where(Appointment.id == appointment_id)
        )
        appointment = session.scalar(statement)
        if appointment is None:
            raise NotFoundError(f"Appointment {appointment_id} was not found.")
        return appointment

    def create_appointment(self, session: Session, payload: AppointmentCreate) -> Appointment:
        """Create and persist an appointment."""
        self._validate_relationships(
            session=session,
            customer_id=payload.customer_id,
            vehicle_id=payload.vehicle_id,
            employee_id=payload.employee_id,
        )
        appointment = Appointment(**payload.model_dump())
        session.add(appointment)
        session.commit()
        session.refresh(appointment)
        return appointment

    def update_appointment(
        self,
        session: Session,
        appointment_id: int,
        payload: AppointmentUpdate,
    ) -> Appointment:
        """Update an existing appointment."""
        appointment = self.get_appointment(session, appointment_id)
        data = payload.model_dump(exclude_unset=True)
        customer_id = data.get("customer_id", appointment.customer_id)
        vehicle_id = data.get("vehicle_id", appointment.vehicle_id)
        employee_id = data.get("employee_id", appointment.employee_id)
        self._validate_relationships(
            session=session,
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            employee_id=employee_id,
        )
        for field, value in data.items():
            setattr(appointment, field, value)
        if appointment.status == AppointmentStatus.COMPLETED and appointment.completed_at is None:
            appointment.completed_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(appointment)
        return appointment

    def update_appointment_status(
        self,
        session: Session,
        appointment_id: int,
        status: AppointmentStatus,
    ) -> Appointment:
        """Update only the appointment status."""
        appointment = self.get_appointment(session, appointment_id)
        appointment.status = status
        if status == AppointmentStatus.COMPLETED:
            appointment.completed_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(appointment)
        return appointment

    def save_appointment_photo(
        self,
        session: Session,
        appointment_id: int,
        tag: AppointmentPhotoTag,
        filename: str,
        content: bytes,
    ) -> AppointmentPhoto:
        """Persist a photo for an existing appointment."""
        appointment = self.get_appointment(session, appointment_id)
        photo = self.photo_storage.save_appointment_photo(
            appointment_id=appointment.id,
            tag=tag,
            filename=filename,
            content=content,
        )
        session.add(photo)
        session.commit()
        session.refresh(photo)
        return photo

    def _validate_relationships(
        self,
        *,
        session: Session,
        customer_id: int,
        vehicle_id: int,
        employee_id: int | None,
    ) -> None:
        """Validate linked records and ownership rules."""
        self.customer_service.get_customer(session, customer_id)
        vehicle = self.vehicle_service.get_vehicle(session, vehicle_id)
        if vehicle.customer_id != customer_id:
            raise ValidationError("Vehicle must belong to the selected customer.")
        if employee_id is not None:
            self.employee_service.get_employee(session, employee_id)
