"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.mcp.server import create_mcp_server
import app.models  # noqa: F401


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    application = FastAPI(title=settings.app_name)
    application.include_router(api_router)
    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    create_mcp_server()

    @application.on_event("startup")
    def initialize_database() -> None:
        """Create database tables for the current metadata set."""
        Base.metadata.create_all(bind=engine)

    return application


app = create_app()
