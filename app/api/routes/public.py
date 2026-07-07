"""Public booking routes."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_appointment_service, get_customer_service, get_vehicle_service
from app.db.session import get_db_session
from app.schemas.appointment import AppointmentCreate
from app.schemas.customer import CustomerCreate
from app.schemas.vehicle import VehicleCreate
from app.services import AppointmentService, CustomerService, VehicleService
from app.web import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def booking_page(
    request: Request,
    customer_service: CustomerService = Depends(get_customer_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Render the public booking page."""
    context = {
        "request": request,
        "customers": customer_service.list_customers(session),
        "vehicles": vehicle_service.list_vehicles(session),
    }
    return templates.TemplateResponse("booking/index.html", context)


@router.post("/booking", response_class=HTMLResponse)
def create_booking(
    request: Request,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_email: str = Form(default=""),
    customer_address: str = Form(...),
    vehicle_make: str = Form(...),
    vehicle_model: str = Form(...),
    vehicle_size: str = Form(...),
    service_name: str = Form(...),
    price_cents: int = Form(...),
    service_address: str = Form(...),
    scheduled_at: str = Form(...),
    customer_service: CustomerService = Depends(get_customer_service),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Create a booking through the public form."""
    customer = customer_service.create_customer(
        session,
        CustomerCreate(
            full_name=customer_name,
            phone=customer_phone,
            email=customer_email or None,
            address=customer_address,
        ),
    )
    vehicle = vehicle_service.create_vehicle(
        session,
        VehicleCreate(
            customer_id=customer.id,
            make=vehicle_make,
            model=vehicle_model,
            vehicle_size=vehicle_size,
        ),
    )
    appointment = appointment_service.create_appointment(
        session,
        AppointmentCreate(
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            scheduled_at=datetime.fromisoformat(scheduled_at),
            service_address=service_address,
            price_cents=price_cents,
            service_name=service_name,
        ),
    )
    return templates.TemplateResponse(
        "booking/_confirmation.html",
        {"request": request, "appointment": appointment, "customer": customer, "vehicle": vehicle},
    )
