"""Service layer for alert operations."""

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from ..models import Alert
from ..schemas import AlertCreate, AlertUpdate


class AlertService:
    """Business logic for alert management."""

    @staticmethod
    def create_alert(db: Session, alert_in: AlertCreate) -> Alert:
        """Create a new alert."""
        alert = Alert(
            id=str(uuid.uuid4()),
            device_id=alert_in.device_id,
            alert_type=alert_in.alert_type,
            severity=alert_in.severity,
            message=alert_in.message,
            threshold_value=alert_in.threshold_value,
            actual_value=alert_in.actual_value,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_alert(db: Session, alert_id: str) -> Optional[Alert]:
        """Get an alert by ID."""
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def get_alerts_by_device(
        db: Session,
        device_id: str,
        skip: int = 0,
        limit: int = 100,
        is_resolved: Optional[bool] = None,
    ) -> List[Alert]:
        """Get alerts for a specific device."""
        query = db.query(Alert).filter(Alert.device_id == device_id)

        if is_resolved is not None:
            query = query.filter(Alert.is_resolved == is_resolved)

        return query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_unresolved_alerts(db: Session, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get all unresolved alerts."""
        return (
            db.query(Alert)
            .filter(Alert.is_resolved == False)
            .order_by(Alert.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_alert(db: Session, alert_id: str, alert_in: AlertUpdate) -> Optional[Alert]:
        """Update an alert."""
        alert = AlertService.get_alert(db, alert_id)
        if not alert:
            return None

        update_data = alert_in.model_dump(exclude_unset=True)
        if "is_resolved" in update_data and update_data["is_resolved"]:
            update_data["resolved_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(alert, field, value)

        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def resolve_alert(db: Session, alert_id: str) -> Optional[Alert]:
        """Mark an alert as resolved."""
        alert = AlertService.get_alert(db, alert_id)
        if not alert:
            return None

        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def delete_alert(db: Session, alert_id: str) -> bool:
        """Delete an alert."""
        alert = AlertService.get_alert(db, alert_id)
        if not alert:
            return False

        db.delete(alert)
        db.commit()
        return True

    @staticmethod
    def get_alert_count(db: Session, is_resolved: Optional[bool] = None) -> int:
        """Get count of alerts."""
        query = db.query(Alert)
        if is_resolved is not None:
            query = query.filter(Alert.is_resolved == is_resolved)
        return query.count()
