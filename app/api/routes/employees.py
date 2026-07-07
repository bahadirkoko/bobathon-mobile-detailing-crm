"""Employee route handlers."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_service
from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.services import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[EmployeeRead])
def list_employees(
    session: Session = Depends(get_db_session),
    service: EmployeeService = Depends(get_employee_service),
) -> list[EmployeeRead]:
    """Return all employees."""
    return [EmployeeRead.model_validate(item) for item in service.list_employees(session)]


@router.post("", response_model=EmployeeRead)
def create_employee(
    payload: EmployeeCreate,
    session: Session = Depends(get_db_session),
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    """Create an employee."""
    employee = service.create_employee(session, payload)
    return EmployeeRead.model_validate(employee)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: int,
    session: Session = Depends(get_db_session),
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    """Return an employee by id."""
    return EmployeeRead.model_validate(service.get_employee(session, employee_id))


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    session: Session = Depends(get_db_session),
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    """Update an employee."""
    employee = service.update_employee(session, employee_id, payload)
    return EmployeeRead.model_validate(employee)
