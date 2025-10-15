"""Service layer for sensor reading operations."""

from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy.orm import Session

from ..models import SensorReading
from ..schemas import SensorReadingCreate


class SensorReadingService:
    """Business logic for sensor reading management."""

    @staticmethod
    def create_reading(db: Session, reading_in: SensorReadingCreate) -> SensorReading:
        """Create a new sensor reading."""
        reading = SensorReading(
            device_id=reading_in.device_id,
            sensor_type=reading_in.sensor_type,
            value=reading_in.value,
            unit=reading_in.unit,
            timestamp=reading_in.timestamp or datetime.utcnow(),
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading

    @staticmethod
    def get_reading(db: Session, reading_id: int) -> Optional[SensorReading]:
        """Get a sensor reading by ID."""
        return db.query(SensorReading).filter(SensorReading.id == reading_id).first()

    @staticmethod
    def get_readings_by_device(
        db: Session,
        device_id: str,
        skip: int = 0,
        limit: int = 100,
        sensor_type: Optional[str] = None,
    ) -> List[SensorReading]:
        """Get sensor readings for a specific device."""
        query = db.query(SensorReading).filter(SensorReading.device_id == device_id)

        if sensor_type:
            query = query.filter(SensorReading.sensor_type == sensor_type)

        return query.order_by(SensorReading.timestamp.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_latest_reading(db: Session, device_id: str, sensor_type: str) -> Optional[SensorReading]:
        """Get the latest reading for a device and sensor type."""
        return (
            db.query(SensorReading)
            .filter(
                SensorReading.device_id == device_id,
                SensorReading.sensor_type == sensor_type,
            )
            .order_by(SensorReading.timestamp.desc())
            .first()
        )

    @staticmethod
    def get_readings_in_range(
        db: Session,
        device_id: str,
        sensor_type: str,
        start_time: datetime,
        end_time: datetime,
    ) -> List[SensorReading]:
        """Get sensor readings within a time range."""
        return (
            db.query(SensorReading)
            .filter(
                SensorReading.device_id == device_id,
                SensorReading.sensor_type == sensor_type,
                SensorReading.timestamp >= start_time,
                SensorReading.timestamp <= end_time,
            )
            .order_by(SensorReading.timestamp.asc())
            .all()
        )

    @staticmethod
    def get_average_value(
        db: Session,
        device_id: str,
        sensor_type: str,
        hours: int = 24,
    ) -> Optional[float]:
        """Get average sensor value for the last N hours."""
        from sqlalchemy import func

        start_time = datetime.utcnow() - timedelta(hours=hours)
        result = (
            db.query(func.avg(SensorReading.value))
            .filter(
                SensorReading.device_id == device_id,
                SensorReading.sensor_type == sensor_type,
                SensorReading.timestamp >= start_time,
            )
            .scalar()
        )
        return result

    @staticmethod
    def delete_old_readings(db: Session, days: int = 30) -> int:
        """Delete sensor readings older than N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = db.query(SensorReading).filter(SensorReading.timestamp < cutoff_date).delete()
        db.commit()
        return deleted
