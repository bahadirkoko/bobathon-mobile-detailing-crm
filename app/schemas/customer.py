"""Customer schemas."""

from pydantic import EmailStr, Field

from app.schemas.base import ORMBaseModel


class CustomerCreate(ORMBaseModel):
    """Payload for creating a customer."""

    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    address: str = Field(min_length=1, max_length=500)


class CustomerUpdate(ORMBaseModel):
    """Payload for updating a customer."""

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    address: str | None = Field(default=None, min_length=1, max_length=500)


class CustomerRead(ORMBaseModel):
    """Serialized customer record."""

    id: int
    full_name: str
    phone: str
    email: EmailStr | None = None
    address: str
