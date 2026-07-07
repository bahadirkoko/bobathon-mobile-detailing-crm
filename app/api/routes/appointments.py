"""Appointment route handlers."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_appointment_service
from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.models.enums import AppointmentPhotoTag, AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentPhotoRead,
    AppointmentRead,
    AppointmentUpdate,
)
from app.services import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> list[AppointmentRead]:
    """Return all appointments."""
    return [AppointmentRead.model_validate(item) for item in service.list_appointments(session)]


@router.post("", response_model=AppointmentRead)
def create_appointment(
    payload: AppointmentCreate,
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentRead:
    """Create an appointment."""
    appointment = service.create_appointment(session, payload)
    return AppointmentRead.model_validate(appointment)


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(
    appointment_id: int,
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentRead:
    """Return an appointment by id."""
    return AppointmentRead.model_validate(service.get_appointment(session, appointment_id))


@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentRead:
    """Update an appointment."""
    appointment = service.update_appointment(session, appointment_id, payload)
    return AppointmentRead.model_validate(appointment)


@router.post("/{appointment_id}/status/{status}", response_model=AppointmentRead)
def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentRead:
    """Update the appointment status."""
    appointment = service.update_appointment_status(session, appointment_id, status)
    return AppointmentRead.model_validate(appointment)


@router.post("/{appointment_id}/photos", response_model=AppointmentPhotoRead)
async def upload_appointment_photo(
    appointment_id: int,
    tag: AppointmentPhotoTag,
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentPhotoRead:
    """Store an appointment photo."""
    photo = service.save_appointment_photo(
        session,
        appointment_id,
        tag,
        file.filename or "upload.jpg",
        await file.read(),
    )
    return AppointmentPhotoRead.model_validate(photo)


@router.get("/{appointment_id}/report", response_model=AppointmentRead)
def get_appointment_report(
    appointment_id: int,
    session: Session = Depends(get_db_session),
    service: AppointmentService = Depends(get_appointment_service),
) -> AppointmentRead:
    """Return report data for a completed appointment."""
    return AppointmentRead.model_validate(service.get_appointment(session, appointment_id))
