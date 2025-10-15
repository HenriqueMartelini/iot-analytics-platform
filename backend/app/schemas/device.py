"""Pydantic schemas for Device model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    """Schema for creating a new device."""

    name: str = Field(..., min_length=1, max_length=255, description="Device name")
    location: str = Field(..., min_length=1, max_length=255, description="Physical location")
    device_type: str = Field(..., min_length=1, max_length=100, description="Device type/category")
    latitude: Optional[float] = Field(None, description="Geographic latitude")
    longitude: Optional[float] = Field(None, description="Geographic longitude")


class DeviceUpdate(BaseModel):
    """Schema for updating an existing device."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None


class DeviceResponse(BaseModel):
    """Schema for device response in API."""

    id: str
    name: str
    location: str
    device_type: str
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
