"""Employee service functions."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.exceptions import NotFoundError


class EmployeeService:
    """Business logic for employee records."""

    def list_employees(self, session: Session) -> list[Employee]:
        """Return all employees ordered by newest first."""
        statement: Select[tuple[Employee]] = select(Employee).order_by(Employee.id.desc())
        return list(session.scalars(statement))

    def get_employee(self, session: Session, employee_id: int) -> Employee:
        """Return an employee by identifier."""
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise NotFoundError(f"Employee {employee_id} was not found.")
        return employee

    def create_employee(self, session: Session, payload: EmployeeCreate) -> Employee:
        """Create and persist an employee."""
        employee = Employee(**payload.model_dump())
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee

    def update_employee(self, session: Session, employee_id: int, payload: EmployeeUpdate) -> Employee:
        """Update an existing employee."""
        employee = self.get_employee(session, employee_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)
        session.commit()
        session.refresh(employee)
        return employee
