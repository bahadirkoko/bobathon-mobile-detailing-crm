"""Service tests for customer workflows."""

from sqlalchemy.orm import Session

from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services import CustomerService, NotFoundError


def test_create_and_update_customer(session: Session, customer_service: CustomerService) -> None:
    """Customers can be created and updated through the service layer."""
    customer = customer_service.create_customer(
        session,
        CustomerCreate(
            first_name="Jane",
            last_name="Doe",
            phone="555-1234",
            email="jane@example.com",
            default_street_address="123 Main St",
            default_city="Austin",
            default_state="TX",
            default_zipcode="78701",
        ),
    )

    updated = customer_service.update_customer(
        session,
        customer.id,
        CustomerUpdate(first_name="Janet"),
    )

    assert updated.first_name == "Janet"
    assert customer_service.list_customers(session)[0].id == customer.id


def test_get_customer_raises_for_unknown_id(
    session: Session,
    customer_service: CustomerService,
) -> None:
    """Unknown customers raise a not-found error."""
    try:
        customer_service.get_customer(session, 999)
    except NotFoundError:
        return
    raise AssertionError("Expected NotFoundError for missing customer")
