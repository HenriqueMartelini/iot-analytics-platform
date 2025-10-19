"""API endpoints for sensor reading management."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import SensorReadingCreate, SensorReadingResponse
from ..services import SensorReadingService
from ..utils import logger

router = APIRouter(prefix="/sensor-readings", tags=["sensor-readings"])


@router.post("", response_model=SensorReadingResponse, status_code=201)
def create_reading(reading_in: SensorReadingCreate, db: Session = Depends(get_db)):
    """Create a new sensor reading."""
    try:
        reading = SensorReadingService.create_reading(db, reading_in)
        logger.info(f"Sensor reading created for device: {reading.device_id}")
        return reading
    except Exception as e:
        logger.error(f"Error creating sensor reading: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating sensor reading")


@router.get("", response_model=List[SensorReadingResponse])
def list_readings(
    device_id: Optional[str] = None,
    sensor_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List sensor readings with optional filtering."""
    try:
        if device_id:
            readings = SensorReadingService.get_readings_by_device(
                db, device_id, skip, limit, sensor_type
            )
        else:
            from sqlalchemy import desc
            query = db.query(SensorReading)
            if sensor_type:
                query = query.filter(SensorReading.sensor_type == sensor_type)
            readings = query.order_by(desc(SensorReading.timestamp)).offset(skip).limit(limit).all()
        return readings
    except Exception as e:
        logger.error(f"Error listing sensor readings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing sensor readings")


@router.get("/{reading_id}", response_model=SensorReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    """Get a specific sensor reading."""
    reading = SensorReadingService.get_reading(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return reading


@router.get("/device/{device_id}/latest", response_model=SensorReadingResponse)
def get_latest_reading(
    device_id: str,
    sensor_type: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get the latest reading for a device and sensor type."""
    try:
        reading = SensorReadingService.get_latest_reading(db, device_id, sensor_type)
        if not reading:
            raise HTTPException(status_code=404, detail="No readings found")
        return reading
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest reading: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting latest reading")


@router.get("/device/{device_id}/average", response_model=dict)
def get_average_value(
    device_id: str,
    sensor_type: str = Query(...),
    hours: int = Query(24, ge=1),
    db: Session = Depends(get_db),
):
    """Get average sensor value for the last N hours."""
    try:
        average = SensorReadingService.get_average_value(db, device_id, sensor_type, hours)
        return {"device_id": device_id, "sensor_type": sensor_type, "average": average, "hours": hours}
    except Exception as e:
        logger.error(f"Error calculating average: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating average")
