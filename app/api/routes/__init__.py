"""API router composition."""

from fastapi import APIRouter

from app.api.routes.appointments import router as appointments_router
from app.api.routes.customers import router as customers_router
from app.api.routes.employees import router as employees_router
from app.api.routes.system import router as system_router
from app.api.routes.vehicles import router as vehicles_router

router = APIRouter()
router.include_router(system_router)
router.include_router(customers_router)
router.include_router(employees_router)
router.include_router(vehicles_router)
router.include_router(appointments_router)
