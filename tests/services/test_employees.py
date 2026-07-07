"""Service tests for employee workflows."""

from datetime import date

from sqlalchemy.orm import Session

from app.models.enums import EmployeeRole
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services import EmployeeService, NotFoundError


def test_create_and_update_employee(session: Session, employee_service: EmployeeService) -> None:
    """Employees can be created and updated through the service layer."""
    employee = employee_service.create_employee(
        session,
        EmployeeCreate(
            first_name="Taylor",
            last_name="Tech",
            role=EmployeeRole.TECHNICIAN,
            phone="555-2222",
            email="tech@example.com",
            hire_date=date(2025, 1, 1),
            is_active=True,
        ),
    )

    updated = employee_service.update_employee(
        session,
        employee.id,
        EmployeeUpdate(role=EmployeeRole.ADMIN, is_active=False),
    )

    assert updated.role == EmployeeRole.ADMIN
    assert updated.is_active is False
    assert employee_service.list_employees(session)[0].id == employee.id


def test_get_employee_raises_for_unknown_id(
    session: Session,
    employee_service: EmployeeService,
) -> None:
    """Unknown employees raise a not-found error."""
    try:
        employee_service.get_employee(session, 999)
    except NotFoundError:
        return
    raise AssertionError("Expected NotFoundError for missing employee")
