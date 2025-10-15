"""Service layer for device-related operations."""

import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from ..models import Device
from ..schemas import DeviceCreate, DeviceUpdate


class DeviceService:
    """Business logic for device management."""

    @staticmethod
    def create_device(db: Session, device_in: DeviceCreate) -> Device:
        """
        Create a new device.
        
        Args:
            db: Database session
            device_in: Device creation data
            
        Returns:
            Device: Created device instance
        """
        device = Device(
            id=str(uuid.uuid4()),
            name=device_in.name,
            location=device_in.location,
            device_type=device_in.device_type,
            latitude=device_in.latitude,
            longitude=device_in.longitude,
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def get_device(db: Session, device_id: str) -> Optional[Device]:
        """Get a device by ID."""
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_devices(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        location: Optional[str] = None,
        device_type: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[Device]:
        """
        Get devices with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            location: Filter by location
            device_type: Filter by device type
            is_active: Filter by active status
            
        Returns:
            List[Device]: List of matching devices
        """
        query = db.query(Device)

        if location:
            query = query.filter(Device.location.ilike(f"%{location}%"))
        if device_type:
            query = query.filter(Device.device_type == device_type)
        if is_active is not None:
            query = query.filter(Device.is_active == is_active)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_device(db: Session, device_id: str, device_in: DeviceUpdate) -> Optional[Device]:
        """Update a device."""
        device = DeviceService.get_device(db, device_id)
        if not device:
            return None

        update_data = device_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)

        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def delete_device(db: Session, device_id: str) -> bool:
        """Delete a device."""
        device = DeviceService.get_device(db, device_id)
        if not device:
            return False

        db.delete(device)
        db.commit()
        return True

    @staticmethod
    def get_device_count(db: Session) -> int:
        """Get total count of devices."""
        return db.query(Device).count()

    @staticmethod
    def get_active_devices(db: Session) -> List[Device]:
        """Get all active devices."""
        return db.query(Device).filter(Device.is_active == True).all()
