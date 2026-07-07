"""Smoke tests for core route modules."""

import importlib


def test_route_modules_import() -> None:
    """Core route modules import successfully."""
    modules = [
        "app.api.routes.public",
        "app.api.routes.system",
        "app.api.routes.dashboard",
        "app.api.routes.admin",
        "app.api.routes.customers",
        "app.api.routes.employees",
        "app.api.routes.vehicles",
        "app.api.routes.appointments",
    ]
    for module in modules:
        assert importlib.import_module(module) is not None
