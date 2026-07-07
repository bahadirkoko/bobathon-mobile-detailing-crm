"""Customer service functions."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.exceptions import NotFoundError


class CustomerService:
    """Business logic for customer records."""

    def list_customers(self, session: Session) -> list[Customer]:
        """Return all customers ordered by newest first."""
        statement: Select[tuple[Customer]] = select(Customer).order_by(Customer.id.desc())
        return list(session.scalars(statement))

    def get_customer(self, session: Session, customer_id: int) -> Customer:
        """Return a customer by identifier."""
        customer = session.get(Customer, customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} was not found.")
        return customer

    def create_customer(self, session: Session, payload: CustomerCreate) -> Customer:
        """Create and persist a customer."""
        customer = Customer(**payload.model_dump())
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    def update_customer(self, session: Session, customer_id: int, payload: CustomerUpdate) -> Customer:
        """Update an existing customer."""
        customer = self.get_customer(session, customer_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(customer, field, value)
        session.commit()
        session.refresh(customer)
        return customer
