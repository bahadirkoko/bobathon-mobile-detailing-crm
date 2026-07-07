"""Shared dependency helpers for routes."""

from app.services import AppointmentService, CustomerService, EmployeeService, VehicleService


def get_customer_service() -> CustomerService:
    """Return the customer service instance."""
    return CustomerService()


def get_employee_service() -> EmployeeService:
    """Return the employee service instance."""
    return EmployeeService()


def get_vehicle_service() -> VehicleService:
    """Return the vehicle service instance."""
    return VehicleService()


def get_appointment_service() -> AppointmentService:
    """Return the appointment service instance."""
    return AppointmentService()
