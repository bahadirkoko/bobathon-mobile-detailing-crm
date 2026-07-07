"""Service tests for appointment workflows."""

from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.enums import AppointmentPhotoTag, AppointmentStatus, EmployeeRole
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.schemas.customer import CustomerCreate
from app.schemas.employee import EmployeeCreate
from app.schemas.vehicle import VehicleCreate
from app.services import (
    AppointmentService,
    CustomerService,
    EmployeeService,
    ValidationError,
    VehicleService,
)


def _seed_dependencies(
    session: Session,
    customer_service: CustomerService,
    employee_service: EmployeeService,
    vehicle_service: VehicleService,
) -> tuple[int, int, int]:
    customer = customer_service.create_customer(
        session,
        CustomerCreate(first_name="Client", last_name="One", phone="555", email=None, default_street_address="123 Main", default_city="Austin", default_state="TX", default_zipcode="78701"),
    )
    employee = employee_service.create_employee(
        session,
        EmployeeCreate(
            first_name="Tech",
            last_name="One",
            role=EmployeeRole.TECHNICIAN,
            phone="777",
            email=None,
        ),
    )
    vehicle = vehicle_service.create_vehicle(
        session,
        VehicleCreate(customer_id=customer.id, make="BMW", model="X5", vehicle_size="suv"),
    )
    return customer.id, employee.id, vehicle.id


def test_create_update_complete_and_photo_upload(
    session: Session,
    appointment_service: AppointmentService,
    customer_service: CustomerService,
    employee_service: EmployeeService,
    vehicle_service: VehicleService,
    upload_root: Path,
) -> None:
    """Appointments support CRUD-like updates, completion, and photo persistence."""
    customer_id, employee_id, vehicle_id = _seed_dependencies(
        session,
        customer_service,
        employee_service,
        vehicle_service,
    )
    appointment = appointment_service.create_appointment(
        session,
        AppointmentCreate(
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            employee_id=employee_id,
            scheduled_at=datetime(2025, 1, 1, 10, 0, 0),
            service_address="123 Detail Lane",
            price_cents=25000,
            service_name="Full Detail",
        ),
    )

    updated = appointment_service.update_appointment(
        session,
        appointment.id,
        AppointmentUpdate(service_name="Interior Detail"),
    )
    completed = appointment_service.update_appointment_status(
        session,
        appointment.id,
        AppointmentStatus.COMPLETED,
    )
    photo = appointment_service.save_appointment_photo(
        session,
        appointment.id,
        AppointmentPhotoTag.BEFORE,
        "before.jpg",
        b"demo-bytes",
    )

    assert updated.service_name == "Interior Detail"
    assert completed.completed_at is not None
    assert photo.file_path.startswith("static/uploads/")
    assert any(upload_root.iterdir())


def test_vehicle_must_belong_to_selected_customer(
    session: Session,
    appointment_service: AppointmentService,
    customer_service: CustomerService,
    employee_service: EmployeeService,
    vehicle_service: VehicleService,
) -> None:
    """Appointments reject mismatched customer and vehicle relationships."""
    customer_id, employee_id, vehicle_id = _seed_dependencies(
        session,
        customer_service,
        employee_service,
        vehicle_service,
    )
    other_customer = customer_service.create_customer(
        session,
        CustomerCreate(
            first_name="Other",
            last_name="Customer",
            phone="999",
            email=None,
            default_street_address="456 Elsewhere",
            default_city="Dallas",
            default_state="TX",
            default_zipcode="75001",
        ),
    )

    try:
        appointment_service.create_appointment(
            session,
            AppointmentCreate(
                customer_id=other_customer.id,
                vehicle_id=vehicle_id,
                employee_id=employee_id,
                scheduled_at=datetime(2025, 1, 1, 10, 0, 0),
                service_address="123 Detail Lane",
                price_cents=25000,
                service_name="Full Detail",
            ),
        )
    except ValidationError:
        return
    raise AssertionError(f"Expected ValidationError for mismatched customer {customer_id}")
