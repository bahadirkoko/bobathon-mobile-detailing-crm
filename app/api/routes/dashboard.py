"""Server-rendered dashboard routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_appointment_service,
    get_customer_service,
    get_employee_service,
    get_vehicle_service,
)
from app.core.auth import DemoUser, get_current_user
from app.db.session import get_db_session
from app.services import AppointmentService, CustomerService, EmployeeService, VehicleService
from app.web import templates

router = APIRouter(include_in_schema=False)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_home(
    request: Request,
    user: DemoUser = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    customer_service: CustomerService = Depends(get_customer_service),
    employee_service: EmployeeService = Depends(get_employee_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the shared dashboard home page."""
    context = {
        "request": request,
        "user": user,
        "appointments": appointment_service.list_appointments(session),
        "customers": customer_service.list_customers(session),
        "employees": employee_service.list_employees(session),
        "vehicles": vehicle_service.list_vehicles(session),
    }
    return templates.TemplateResponse("dashboard/index.html", context)
