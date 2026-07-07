"""Shared model enums."""

from enum import StrEnum


class EmployeeRole(StrEnum):
    """Supported employee roles for the MVP."""

    ADMIN = "admin"
    TECHNICIAN = "technician"


class AppointmentStatus(StrEnum):
    """Supported appointment states for the MVP."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AppointmentPhotoTag(StrEnum):
    """Supported appointment photo labels."""

    BEFORE = "before"
    AFTER = "after"
