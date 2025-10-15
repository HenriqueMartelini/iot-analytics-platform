"""Database models for IoT Analytics Platform."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .device import Device
from .sensor_reading import SensorReading
from .alert import Alert

__all__ = ["Base", "Device", "SensorReading", "Alert"]
