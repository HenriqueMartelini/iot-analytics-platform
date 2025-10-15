"""API route modules."""

from .devices import router as devices_router
from .sensor_readings import router as sensor_readings_router
from .alerts import router as alerts_router
from .health import router as health_router

__all__ = ["devices_router", "sensor_readings_router", "alerts_router", "health_router"]
