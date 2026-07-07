"""MCP server bootstrap and tool registration."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.enums import AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from app.services import AppointmentService, CustomerService, EmployeeService, VehicleService

mcp = FastMCP(name="mobile-detailing-crm")


@contextmanager
def managed_session() -> Session:
    """Provide a managed database session for MCP tools."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@mcp.tool()
def list_customers() -> list[dict[str, Any]]:
    """List all customers."""
    with managed_session() as session:
        customers = CustomerService().list_customers(session)
        return [CustomerRead.model_validate(item).model_dump(mode="json") for item in customers]


@mcp.tool()
def create_customer(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a customer."""
    with managed_session() as session:
        customer = CustomerService().create_customer(session, CustomerCreate.model_validate(payload))
        return CustomerRead.model_validate(customer).model_dump(mode="json")


@mcp.tool()
def update_customer(customer_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    """Update a customer."""
    with managed_session() as session:
        customer = CustomerService().update_customer(
            session,
            customer_id,
            CustomerUpdate.model_validate(payload),
        )
        return CustomerRead.model_validate(customer).model_dump(mode="json")


@mcp.tool()
def list_employees() -> list[dict[str, Any]]:
    """List all employees."""
    with managed_session() as session:
        employees = EmployeeService().list_employees(session)
        return [EmployeeRead.model_validate(item).model_dump(mode="json") for item in employees]


@mcp.tool()
def create_employee(payload: dict[str, Any]) -> dict[str, Any]:
    """Create an employee."""
    with managed_session() as session:
        employee = EmployeeService().create_employee(session, EmployeeCreate.model_validate(payload))
        return EmployeeRead.model_validate(employee).model_dump(mode="json")


@mcp.tool()
def update_employee(employee_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    """Update an employee."""
    with managed_session() as session:
        employee = EmployeeService().update_employee(
            session,
            employee_id,
            EmployeeUpdate.model_validate(payload),
        )
        return EmployeeRead.model_validate(employee).model_dump(mode="json")


@mcp.tool()
def list_vehicles() -> list[dict[str, Any]]:
    """List all vehicles."""
    with managed_session() as session:
        vehicles = VehicleService().list_vehicles(session)
        return [VehicleRead.model_validate(item).model_dump(mode="json") for item in vehicles]


@mcp.tool()
def create_vehicle(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a vehicle."""
    with managed_session() as session:
        vehicle = VehicleService().create_vehicle(session, VehicleCreate.model_validate(payload))
        return VehicleRead.model_validate(vehicle).model_dump(mode="json")


@mcp.tool()
def update_vehicle(vehicle_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    """Update a vehicle."""
    with managed_session() as session:
        vehicle = VehicleService().update_vehicle(
            session,
            vehicle_id,
            VehicleUpdate.model_validate(payload),
        )
        return VehicleRead.model_validate(vehicle).model_dump(mode="json")


@mcp.tool()
def list_appointments() -> list[dict[str, Any]]:
    """List all appointments."""
    with managed_session() as session:
        appointments = AppointmentService().list_appointments(session)
        return [AppointmentRead.model_validate(item).model_dump(mode="json") for item in appointments]


@mcp.tool()
def create_appointment(payload: dict[str, Any]) -> dict[str, Any]:
    """Create an appointment."""
    with managed_session() as session:
        appointment = AppointmentService().create_appointment(
            session,
            AppointmentCreate.model_validate(payload),
        )
        return AppointmentRead.model_validate(appointment).model_dump(mode="json")


@mcp.tool()
def update_appointment(appointment_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    """Update an appointment."""
    with managed_session() as session:
        appointment = AppointmentService().update_appointment(
            session,
            appointment_id,
            AppointmentUpdate.model_validate(payload),
        )
        return AppointmentRead.model_validate(appointment).model_dump(mode="json")


@mcp.tool()
def update_appointment_status(appointment_id: int, status: str) -> dict[str, Any]:
    """Update only the appointment status."""
    with managed_session() as session:
        appointment = AppointmentService().update_appointment_status(
            session,
            appointment_id,
            AppointmentStatus(status),
        )
        return AppointmentRead.model_validate(appointment).model_dump(mode="json")


def create_mcp_server() -> FastMCP:
    """Return the configured MCP server instance."""
    return mcp
