"""System and public utility routes."""

from fastapi import APIRouter, Depends

from app.core.auth import DemoUser, get_current_user

router = APIRouter(tags=["system"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    """Return a simple health response."""
    return {"status": "ok"}


@router.get("/me")
def get_me(user: DemoUser = Depends(get_current_user)) -> dict[str, str]:
    """Return the current demo user information."""
    return {"email": user.email, "role": user.role, "full_name": user.full_name}
