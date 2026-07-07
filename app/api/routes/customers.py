"""Customer route handlers."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_customer_service
from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.services import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[CustomerRead])
def list_customers(
    session: Session = Depends(get_db_session),
    service: CustomerService = Depends(get_customer_service),
) -> list[CustomerRead]:
    """Return all customers."""
    return [CustomerRead.model_validate(item) for item in service.list_customers(session)]


@router.post("", response_model=CustomerRead)
def create_customer(
    payload: CustomerCreate,
    session: Session = Depends(get_db_session),
    service: CustomerService = Depends(get_customer_service),
) -> CustomerRead:
    """Create a customer."""
    customer = service.create_customer(session, payload)
    return CustomerRead.model_validate(customer)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(
    customer_id: int,
    session: Session = Depends(get_db_session),
    service: CustomerService = Depends(get_customer_service),
) -> CustomerRead:
    """Return a customer by id."""
    return CustomerRead.model_validate(service.get_customer(session, customer_id))


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    session: Session = Depends(get_db_session),
    service: CustomerService = Depends(get_customer_service),
) -> CustomerRead:
    """Update a customer."""
    customer = service.update_customer(session, customer_id, payload)
    return CustomerRead.model_validate(customer)
