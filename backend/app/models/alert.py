"""Alert model for threshold violations and anomalies."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from . import Base


class Alert(Base):
    """
    Alert model for device threshold violations.
    
    Tracks alerts generated when sensor readings exceed defined thresholds
    or when anomalies are detected.
    
    Attributes:
        id: Unique identifier for the alert
        device_id: Foreign key reference to the device
        alert_type: Category of alert
        severity: Alert severity level (LOW, MEDIUM, HIGH, CRITICAL)
        message: Human-readable alert description
        threshold_value: The threshold that was exceeded
        actual_value: The actual measured value
        is_resolved: Whether the alert has been resolved
        created_at: When the alert was created
        resolved_at: When the alert was resolved
    """

    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, index=True)
    device_id = Column(String(36), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    message = Column(String(500), nullable=False)
    threshold_value = Column(Float, nullable=True)
    actual_value = Column(Float, nullable=True)
    is_resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    device = relationship("Device", back_populates="alerts")

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, device_id={self.device_id}, severity={self.severity})>"
