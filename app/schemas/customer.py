"""Customer schemas."""

from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import ORMBaseModel


class CustomerCreate(ORMBaseModel):
    """Payload for creating a customer."""

    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    default_street_address: str = Field(min_length=1, max_length=255)
    default_city: str = Field(min_length=1, max_length=255)
    default_state: str = Field(min_length=1, max_length=100)
    default_zipcode: str = Field(min_length=1, max_length=50)


class CustomerUpdate(ORMBaseModel):
    """Payload for updating a customer."""

    first_name: str | None = Field(default=None, min_length=1, max_length=255)
    last_name: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    default_street_address: str | None = Field(default=None, min_length=1, max_length=255)
    default_city: str | None = Field(default=None, min_length=1, max_length=255)
    default_state: str | None = Field(default=None, min_length=1, max_length=100)
    default_zipcode: str | None = Field(default=None, min_length=1, max_length=50)


class CustomerRead(ORMBaseModel):
    """Serialized customer record."""

    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr | None = None
    default_street_address: str
    default_city: str
    default_state: str
    default_zipcode: str
    created_at: datetime
    updated_at: datetime
