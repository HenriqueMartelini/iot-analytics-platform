"""Script to seed the database with sample data."""

import sys
from datetime import datetime, timedelta
import random

sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Device, SensorReading, Alert
from app.services import DeviceService, SensorReadingService, AlertService
from app.schemas import DeviceCreate, SensorReadingCreate, AlertCreate

def seed_database():
    """Populate database with sample data."""
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        devices_data = [
            {"name": "Temperature Sensor 1", "device_type": "sensor", "location": "Building A - Floor 1"},
            {"name": "Humidity Sensor 1", "device_type": "sensor", "location": "Building A - Floor 1"},
            {"name": "Temperature Sensor 2", "device_type": "sensor", "location": "Building B - Floor 2"},
            {"name": "Motion Detector 1", "device_type": "motion", "location": "Building A - Entrance"},
        ]
        
        devices = []
        for device_data in devices_data:
            device = DeviceService.create_device(db, DeviceCreate(**device_data))
            devices.append(device)
            print(f"Created device: {device.name}")
        
        base_time = datetime.utcnow() - timedelta(hours=24)
        
        for device in devices:
            if "Temperature" in device.name:
                for i in range(24):
                    timestamp = base_time + timedelta(hours=i)
                    temp_value = 20 + random.uniform(-5, 10)
                    SensorReadingService.create_reading(
                        db,
                        SensorReadingCreate(
                            device_id=device.id,
                            sensor_type="temperature",
                            value=round(temp_value, 2),
                            unit="°C",
                            timestamp=timestamp,
                        )
                    )
                print(f"Created temperature readings for {device.name}")
            
            if "Humidity" in device.name:
                for i in range(24):
                    timestamp = base_time + timedelta(hours=i)
                    humidity_value = 40 + random.uniform(-10, 20)
                    SensorReadingService.create_reading(
                        db,
                        SensorReadingCreate(
                            device_id=device.id,
                            sensor_type="humidity",
                            value=round(humidity_value, 2),
                            unit="%",
                            timestamp=timestamp,
                        )
                    )
                print(f"Created humidity readings for {device.name}")
        
        alerts_data = [
            {
                "device_id": devices[0].id,
                "alert_type": "High Temperature",
                "severity": "MEDIUM",
                "message": "Temperature exceeded threshold",
                "threshold_value": 25.0,
                "actual_value": 27.5,
            },
            {
                "device_id": devices[1].id,
                "alert_type": "Low Humidity",
                "severity": "LOW",
                "message": "Humidity below recommended level",
                "threshold_value": 45.0,
                "actual_value": 38.0,
            },
        ]
        
        for alert_data in alerts_data:
            AlertService.create_alert(db, AlertCreate(**alert_data))
            print(f"Created alert: {alert_data['alert_type']}")
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
