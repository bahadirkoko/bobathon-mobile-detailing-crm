"""Dashboard CRUD page routes and HTMX partials."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
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
from app.models.enums import AppointmentPhotoTag, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services import AppointmentService, CustomerService, EmployeeService, VehicleService
from app.web import templates

router = APIRouter(prefix="/dashboard", include_in_schema=False, dependencies=[Depends(get_current_user)])


@router.get("/customers", response_class=HTMLResponse)
def customers_page(
    request: Request,
    user: DemoUser = Depends(get_current_user),
    customer_service: CustomerService = Depends(get_customer_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the customer management page."""
    return templates.TemplateResponse(
        request,
        "dashboard/customers.html",
        {"request": request, "user": user, "customers": customer_service.list_customers(session)},
    )


@router.post("/customers", response_class=HTMLResponse)
def create_customer_partial(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(default=""),
    default_street_address: str = Form(...),
    default_city: str = Form(...),
    default_state: str = Form(...),
    default_zipcode: str = Form(...),
    customer_service: CustomerService = Depends(get_customer_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Create a customer and return the updated customer list partial."""
    customer_service.create_customer(
        session,
        CustomerCreate(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email or None,
            default_street_address=default_street_address,
            default_city=default_city,
            default_state=default_state,
            default_zipcode=default_zipcode,
        ),
    )
    customers = customer_service.list_customers(session)
    return templates.TemplateResponse(
        request,
        "dashboard/partials/customer_list.html",
        {"request": request, "customers": customers},
    )


@router.post("/customers/{customer_id}/edit", response_class=HTMLResponse)
def update_customer_partial(
    request: Request,
    customer_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(default=""),
    default_street_address: str = Form(...),
    default_city: str = Form(...),
    default_state: str = Form(...),
    default_zipcode: str = Form(...),
    customer_service: CustomerService = Depends(get_customer_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Update a customer and return the updated customer list partial."""
    customer_service.update_customer(
        session,
        customer_id,
        CustomerUpdate(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email or None,
            default_street_address=default_street_address,
            default_city=default_city,
            default_state=default_state,
            default_zipcode=default_zipcode,
        ),
    )
    customers = customer_service.list_customers(session)
    return templates.TemplateResponse(
        request,
        "dashboard/partials/customer_list.html",
        {"request": request, "customers": customers},
    )


@router.get("/appointments", response_class=HTMLResponse)
def appointments_page(
    request: Request,
    user: DemoUser = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    customer_service: CustomerService = Depends(get_customer_service),
    employee_service: EmployeeService = Depends(get_employee_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the appointment management page."""
    context = {
        "request": request,
        "user": user,
        "appointments": appointment_service.list_appointments(session),
        "customers": customer_service.list_customers(session),
        "employees": employee_service.list_employees(session),
        "vehicles": vehicle_service.list_vehicles(session),
        "statuses": list(AppointmentStatus),
    }
    return templates.TemplateResponse(request, "dashboard/appointments.html", context)


@router.post("/appointments", response_class=HTMLResponse)
def create_appointment_partial(
    request: Request,
    customer_id: int = Form(...),
    vehicle_id: int = Form(...),
    employee_id: int | None = Form(default=None),
    scheduled_at: str = Form(...),
    service_address: str = Form(...),
    price_cents: int = Form(...),
    service_name: str = Form(...),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Create an appointment and return the updated appointment list partial."""
    appointment_service.create_appointment(
        session,
        AppointmentCreate(
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            employee_id=employee_id,
            scheduled_at=datetime.fromisoformat(scheduled_at),
            service_address=service_address,
            price_cents=price_cents,
            service_name=service_name,
        ),
    )
    appointments = appointment_service.list_appointments(session)
    return templates.TemplateResponse(
        request,
        "dashboard/partials/appointment_list.html",
        {"request": request, "appointments": appointments},
    )


@router.post("/appointments/{appointment_id}/status", response_class=HTMLResponse)
def update_appointment_status_partial(
    request: Request,
    appointment_id: int,
    status: AppointmentStatus = Form(...),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Update appointment status and return the updated appointment list partial."""
    appointment_service.update_appointment_status(session, appointment_id, status)
    appointments = appointment_service.list_appointments(session)
    return templates.TemplateResponse(
        request,
        "dashboard/partials/appointment_list.html",
        {"request": request, "appointments": appointments},
    )


@router.get("/vehicles", response_class=HTMLResponse)
def vehicles_page(
    request: Request,
    user: DemoUser = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the vehicle list page."""
    return templates.TemplateResponse(
        request,
        "dashboard/vehicles.html",
        {"request": request, "user": user, "vehicles": vehicle_service.list_vehicles(session)},
    )


@router.get("/employees", response_class=HTMLResponse)
def employees_page(
    request: Request,
    user: DemoUser = Depends(get_current_user),
    employee_service: EmployeeService = Depends(get_employee_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the employee list page."""
    return templates.TemplateResponse(
        request,
        "dashboard/employees.html",
        {"request": request, "user": user, "employees": employee_service.list_employees(session)},
    )


@router.post("/appointments/{appointment_id}/photos", response_class=HTMLResponse)
async def upload_appointment_photo_partial(
    request: Request,
    appointment_id: int,
    tag: AppointmentPhotoTag = Form(...),
    photo: UploadFile = File(...),
    user: DemoUser = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Upload a photo and re-render the report page."""
    appointment_service.save_appointment_photo(
        session,
        appointment_id,
        tag,
        photo.filename or "upload.jpg",
        await photo.read(),
    )
    appointment = appointment_service.get_appointment(session, appointment_id)
    return templates.TemplateResponse(
        request,
        "reports/appointment_report.html",
        {"request": request, "user": user, "appointment": appointment},
    )


@router.get("/appointments/{appointment_id}/report", response_class=HTMLResponse)
def appointment_report_page(
    request: Request,
    appointment_id: int,
    user: DemoUser = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the completed appointment report page."""
    appointment = appointment_service.get_appointment(session, appointment_id)
    return templates.TemplateResponse(
        request,
        "reports/appointment_report.html",
        {"request": request, "user": user, "appointment": appointment},
    )
