"""Pydantic schemas for SensorReading model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorReadingCreate(BaseModel):
    """Schema for creating a new sensor reading."""

    device_id: str = Field(..., description="Device ID")
    sensor_type: str = Field(..., min_length=1, max_length=100, description="Type of sensor")
    value: float = Field(..., description="Measured value")
    unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    timestamp: Optional[datetime] = Field(None, description="Measurement timestamp")


class SensorReadingResponse(BaseModel):
    """Schema for sensor reading response in API."""

    id: int
    device_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True
