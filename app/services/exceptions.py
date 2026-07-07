"""Application-level service exceptions."""


class ServiceError(Exception):
    """Base exception for service-layer failures."""


class NotFoundError(ServiceError):
    """Raised when a requested resource does not exist."""


class ValidationError(ServiceError):
    """Raised when business validation fails."""
