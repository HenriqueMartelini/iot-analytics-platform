"""API endpoints for device management."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from ..services import DeviceService
from ..utils import logger

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("", response_model=DeviceResponse, status_code=201)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device."""
    try:
        device = DeviceService.create_device(db, device_in)
        logger.info(f"Device created: {device.id}")
        return device
    except Exception as e:
        logger.error(f"Error creating device: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating device")


@router.get("", response_model=List[DeviceResponse])
def list_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    location: Optional[str] = None,
    device_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List all devices with optional filtering."""
    try:
        devices = DeviceService.get_devices(
            db,
            skip=skip,
            limit=limit,
            location=location,
            device_type=device_type,
            is_active=is_active,
        )
        return devices
    except Exception as e:
        logger.error(f"Error listing devices: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing devices")


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """Get a specific device by ID."""
    device = DeviceService.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
):
    """Update a device."""
    try:
        device = DeviceService.update_device(db, device_id, device_in)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        logger.info(f"Device updated: {device_id}")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating device: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating device")


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """Delete a device."""
    try:
        success = DeviceService.delete_device(db, device_id)
        if not success:
            raise HTTPException(status_code=404, detail="Device not found")
        logger.info(f"Device deleted: {device_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting device: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting device")


@router.get("/stats/count", response_model=dict)
def get_device_stats(db: Session = Depends(get_db)):
    """Get device statistics."""
    try:
        total = DeviceService.get_device_count(db)
        active = len(DeviceService.get_active_devices(db))
        return {"total": total, "active": active}
    except Exception as e:
        logger.error(f"Error getting device stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting device stats")
