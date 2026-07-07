"""Service tests for vehicle workflows."""

from sqlalchemy.orm import Session

from app.schemas.customer import CustomerCreate
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.services import CustomerService, NotFoundError, ValidationError, VehicleService


def test_create_and_update_vehicle(
    session: Session,
    customer_service: CustomerService,
    vehicle_service: VehicleService,
) -> None:
    """Vehicles can be created and updated when the customer exists."""
    customer = customer_service.create_customer(
        session,
        CustomerCreate(first_name="Driver", last_name="One", phone="555", email=None, default_street_address="123 Main", default_city="Austin", default_state="TX", default_zipcode="78701"),
    )

    vehicle = vehicle_service.create_vehicle(
        session,
        VehicleCreate(customer_id=customer.id, make="Tesla", model="Model 3", vehicle_size="sedan"),
    )
    updated = vehicle_service.update_vehicle(
        session,
        vehicle.id,
        VehicleUpdate(color="Blue"),
    )

    assert updated.color == "Blue"
    assert vehicle_service.list_vehicles(session)[0].id == vehicle.id


def test_create_vehicle_requires_known_customer(
    session: Session,
    vehicle_service: VehicleService,
) -> None:
    """Vehicles require a valid customer relationship."""
    try:
        vehicle_service.create_vehicle(
            session,
            VehicleCreate(customer_id=999, make="Ford", model="F-150", vehicle_size="truck"),
        )
    except NotFoundError:
        return
    raise AssertionError("Expected NotFoundError for missing customer")
