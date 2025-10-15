"""Pydantic schemas for Alert model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    """Schema for creating a new alert."""

    device_id: str = Field(..., description="Device ID")
    alert_type: str = Field(..., min_length=1, max_length=100, description="Alert type")
    severity: str = Field(..., regex="^(LOW|MEDIUM|HIGH|CRITICAL)$", description="Alert severity")
    message: str = Field(..., min_length=1, max_length=500, description="Alert message")
    threshold_value: Optional[float] = Field(None, description="Threshold value")
    actual_value: Optional[float] = Field(None, description="Actual measured value")


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""

    is_resolved: Optional[bool] = Field(None, description="Resolution status")
    severity: Optional[str] = Field(None, regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")


class AlertResponse(BaseModel):
    """Schema for alert response in API."""

    id: str
    device_id: str
    alert_type: str
    severity: str
    message: str
    threshold_value: Optional[float] = None
    actual_value: Optional[float] = None
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
