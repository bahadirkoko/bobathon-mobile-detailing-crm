"""Package service functions."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.package import Package
from app.schemas.package import PackageCreate, PackageUpdate
from app.services.exceptions import NotFoundError


class PackageService:
    """Business logic for package records."""

    def list_packages(self, session: Session) -> list[Package]:
        """Return all packages ordered by newest first."""
        statement: Select[tuple[Package]] = select(Package).order_by(Package.id.desc())
        return list(session.scalars(statement))

    def get_package(self, session: Session, package_id: int) -> Package:
        """Return a package by identifier."""
        package = session.get(Package, package_id)
        if package is None:
            raise NotFoundError(f"Package {package_id} was not found.")
        return package

    def create_package(self, session: Session, payload: PackageCreate) -> Package:
        """Create and persist a package."""
        package = Package(**payload.model_dump())
        session.add(package)
        session.commit()
        session.refresh(package)
        return package

    def update_package(self, session: Session, package_id: int, payload: PackageUpdate) -> Package:
        """Update an existing package."""
        package = self.get_package(session, package_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(package, field, value)
        session.commit()
        session.refresh(package)
        return package

    def delete_package(self, session: Session, package_id: int) -> None:
        """Delete an existing package."""
        package = self.get_package(session, package_id)
        session.delete(package)
        session.commit()
