"""Shared pytest fixtures for the CRM test suite."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models import Appointment, AppointmentPhoto, Customer, Employee, Package, Vehicle
from app.services import (
    AppointmentService,
    AppointmentPhotoStorageService,
    CustomerService,
    EmployeeService,
    PackageService,
    VehicleService,
)


@pytest.fixture()
def session() -> Generator[Session, None, None]:
    """Provide an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    local_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    db_session = local_session()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture()
def upload_root(tmp_path: Path) -> Path:
    """Provide a temporary upload directory for photo storage tests."""
    root = tmp_path / "uploads"
    root.mkdir(parents=True, exist_ok=True)
    return root


@pytest.fixture()
def customer_service() -> CustomerService:
    """Provide the customer service instance."""
    return CustomerService()


@pytest.fixture()
def employee_service() -> EmployeeService:
    """Provide the employee service instance."""
    return EmployeeService()


@pytest.fixture()
def package_service() -> PackageService:
    """Provide the package service instance."""
    return PackageService()


@pytest.fixture()
def vehicle_service(customer_service: CustomerService) -> VehicleService:
    """Provide the vehicle service instance."""
    return VehicleService(customer_service)


@pytest.fixture()
def appointment_service(
    customer_service: CustomerService,
    employee_service: EmployeeService,
    package_service: PackageService,
    vehicle_service: VehicleService,
    upload_root: Path,
) -> AppointmentService:
    """Provide the appointment service instance."""
    storage = AppointmentPhotoStorageService(str(upload_root))
    return AppointmentService(customer_service, employee_service, vehicle_service, package_service, storage)
