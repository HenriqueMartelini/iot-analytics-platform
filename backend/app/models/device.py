"""Device model representing an IoT device in the system."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class Device(Base):
    """
    Device model representing an IoT device.
    
    Attributes:
        id: Unique identifier for the device
        name: Human-readable device name
        location: Physical location of the device
        device_type: Type/category of the device
        status: Current operational status
        latitude: Geographic latitude coordinate
        longitude: Geographic longitude coordinate
        is_active: Whether the device is currently active
        created_at: Timestamp when device was created
        updated_at: Timestamp of last update
    """

    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    device_type = Column(String(100), nullable=False)
    status = Column(String(50), default="active", nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    sensor_readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Device(id={self.id}, name={self.name}, location={self.location})>"
