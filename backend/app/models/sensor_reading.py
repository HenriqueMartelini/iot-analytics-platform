"""Sensor reading model for storing IoT device measurements."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer, Index
from sqlalchemy.orm import relationship

from . import Base


class SensorReading(Base):
    """
    Sensor reading model for IoT device measurements.
    
    Stores individual sensor readings with timestamps and values.
    Includes indexes for efficient querying by device and time.
    
    Attributes:
        id: Unique identifier for the reading
        device_id: Foreign key reference to the device
        sensor_type: Type of sensor (e.g., temperature, humidity)
        value: The measured value
        unit: Unit of measurement (e.g., Celsius, percentage)
        timestamp: When the reading was taken
        created_at: When the record was created
    """

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(36), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True)
    sensor_type = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    device = relationship("Device", back_populates="sensor_readings")

    # Composite indexes for common query patterns
    __table_args__ = (
        Index("idx_device_timestamp", "device_id", "timestamp"),
        Index("idx_sensor_type_timestamp", "sensor_type", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<SensorReading(device_id={self.device_id}, sensor_type={self.sensor_type}, value={self.value})>"
