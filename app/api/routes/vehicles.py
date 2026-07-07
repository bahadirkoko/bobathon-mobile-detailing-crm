"""Vehicle route handlers."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_vehicle_service
from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from app.services import VehicleService

router = APIRouter(prefix="/vehicles", tags=["vehicles"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[VehicleRead])
def list_vehicles(
    session: Session = Depends(get_db_session),
    service: VehicleService = Depends(get_vehicle_service),
) -> list[VehicleRead]:
    """Return all vehicles."""
    return [VehicleRead.model_validate(item) for item in service.list_vehicles(session)]


@router.post("", response_model=VehicleRead)
def create_vehicle(
    payload: VehicleCreate,
    session: Session = Depends(get_db_session),
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleRead:
    """Create a vehicle."""
    vehicle = service.create_vehicle(session, payload)
    return VehicleRead.model_validate(vehicle)


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(
    vehicle_id: int,
    session: Session = Depends(get_db_session),
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleRead:
    """Return a vehicle by id."""
    return VehicleRead.model_validate(service.get_vehicle(session, vehicle_id))


@router.put("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    session: Session = Depends(get_db_session),
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleRead:
    """Update a vehicle."""
    vehicle = service.update_vehicle(session, vehicle_id, payload)
    return VehicleRead.model_validate(vehicle)
