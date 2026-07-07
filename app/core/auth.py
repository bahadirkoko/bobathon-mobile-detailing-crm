"""Demo authentication and session helpers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fastapi import Depends, HTTPException, Request, status

from app.core.config import get_settings


class UserRole(StrEnum):
    """Supported demo session roles."""

    ADMIN = "admin"
    EMPLOYEE = "employee"


@dataclass(slots=True)
class DemoUser:
    """Simple authenticated user representation."""

    email: str
    role: UserRole
    full_name: str


_DEMO_USERS = {
    "admin@example.com": DemoUser(
        email="admin@example.com",
        role=UserRole.ADMIN,
        full_name="Demo Admin",
    ),
    "employee@example.com": DemoUser(
        email="employee@example.com",
        role=UserRole.EMPLOYEE,
        full_name="Demo Employee",
    ),
}


def get_demo_users() -> dict[str, DemoUser]:
    """Return configured demo users keyed by email."""
    settings = get_settings()
    users = dict(_DEMO_USERS)
    users[settings.demo_admin_email] = DemoUser(
        email=settings.demo_admin_email,
        role=UserRole.ADMIN,
        full_name="Demo Admin",
    )
    users[settings.demo_employee_email] = DemoUser(
        email=settings.demo_employee_email,
        role=UserRole.EMPLOYEE,
        full_name="Demo Employee",
    )
    return users


def get_current_user(request: Request) -> DemoUser:
    """Resolve the current demo user from a request header."""
    email = request.headers.get("X-Demo-User")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing demo user.")
    user = get_demo_users().get(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown demo user.")
    return user


def require_admin(user: DemoUser = Depends(get_current_user)) -> DemoUser:
    """Require an admin demo user."""
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    return user
