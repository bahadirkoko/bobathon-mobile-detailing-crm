"""Public booking routes."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_appointment_service,
    get_customer_service,
    get_package_service,
    get_vehicle_service,
)
from app.db.session import get_db_session
from app.schemas.appointment import AppointmentCreate
from app.schemas.customer import CustomerCreate
from app.schemas.vehicle import VehicleCreate
from app.services import AppointmentService, CustomerService, PackageService, VehicleService
from app.web import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def booking_page(
    request: Request,
    customer_service: CustomerService = Depends(get_customer_service),
    package_service: PackageService = Depends(get_package_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the public booking page."""
    context = {
        "request": request,
        "customers": customer_service.list_customers(session),
        "packages": package_service.list_packages(session),
        "vehicles": vehicle_service.list_vehicles(session),
    }
    return templates.TemplateResponse(request, "booking/index.html", context)


@router.post("/booking", response_class=HTMLResponse)
def create_booking(
    request: Request,
    customer_first_name: str = Form(...),
    customer_last_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_email: str = Form(default=""),
    customer_street_address: str = Form(...),
    customer_city: str = Form(...),
    customer_state: str = Form(...),
    customer_zipcode: str = Form(...),
    vehicle_make: str = Form(...),
    vehicle_model: str = Form(...),
    vehicle_type: str = Form(...),
    package_id: int = Form(...),
    appointment_date: str = Form(...),
    appointment_hour: int = Form(...),
    customer_service: CustomerService = Depends(get_customer_service),
    package_service: PackageService = Depends(get_package_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Create a booking through the public form."""
    customer = customer_service.create_customer(
        session,
        CustomerCreate(
            first_name=customer_first_name,
            last_name=customer_last_name,
            phone=customer_phone,
            email=customer_email or None,
            default_street_address=customer_street_address,
            default_city=customer_city,
            default_state=customer_state,
            default_zipcode=customer_zipcode,
        ),
    )
    vehicle = vehicle_service.create_vehicle(
        session,
        VehicleCreate(
            customer_id=customer.id,
            make=vehicle_make,
            model=vehicle_model,
            vehicle_type=vehicle_type,
        ),
    )
    package = package_service.get_package(session, package_id)
    scheduled_at = datetime.fromisoformat(f"{appointment_date}T{appointment_hour:02d}:00:00")
    appointment = appointment_service.create_appointment(
        session,
        AppointmentCreate(
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            package_id=package.id,
            scheduled_at=scheduled_at,
            service_address=(
                f"{customer_street_address}, {customer_city}, {customer_state} {customer_zipcode}"
            ),
            price_cents=package.base_price_cents,
        ),
    )
    return templates.TemplateResponse(
        request,
        "booking/_confirmation.html",
        {"request": request, "appointment": appointment, "customer": customer, "vehicle": vehicle},
    )
