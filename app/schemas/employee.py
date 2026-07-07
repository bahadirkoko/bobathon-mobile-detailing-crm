"""Employee schemas."""

from datetime import date, datetime

from pydantic import EmailStr, Field

from app.models.enums import EmployeeRole
from app.schemas.base import ORMBaseModel


class EmployeeCreate(ORMBaseModel):
    """Payload for creating an employee."""

    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    role: EmployeeRole
    phone: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    hire_date: date | None = None
    is_active: bool = True


class EmployeeUpdate(ORMBaseModel):
    """Payload for updating an employee."""

    first_name: str | None = Field(default=None, min_length=1, max_length=255)
    last_name: str | None = Field(default=None, min_length=1, max_length=255)
    role: EmployeeRole | None = None
    phone: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    hire_date: date | None = None
    is_active: bool | None = None


class EmployeeRead(ORMBaseModel):
    """Serialized employee record."""

    id: int
    first_name: str
    last_name: str
    role: EmployeeRole
    phone: str
    email: EmailStr | None = None
    hire_date: date | None = None
    is_active: bool
    created_at: datetime
