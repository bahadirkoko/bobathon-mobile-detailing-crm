"""System and public utility routes."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.auth import (
    SESSION_COOKIE_NAME,
    DemoUser,
    create_session_cookie_value,
    get_current_user,
    get_demo_users,
)
from app.web import templates

router = APIRouter(tags=["system"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    """Return a simple health response."""
    return {"status": "ok"}


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    """Render the demo login page."""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "demo_users": get_demo_users().values()},
    )


@router.post("/login")
def login_submit(email: str = Form(...)) -> RedirectResponse:
    """Set the signed demo session cookie and redirect to the dashboard."""
    if email not in get_demo_users():
        response = RedirectResponse(url="/login", status_code=303)
        return response

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_session_cookie_value(email),
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/logout")
def logout() -> RedirectResponse:
    """Clear the demo session cookie and redirect to login."""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@router.get("/me")
def get_me(user: DemoUser = Depends(get_current_user)) -> dict[str, str]:
    """Return the current demo user information."""
    return {"email": user.email, "role": user.role, "full_name": user.full_name}
