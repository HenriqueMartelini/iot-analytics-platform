"""API endpoints for alert management."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import AlertCreate, AlertResponse, AlertUpdate
from ..services import AlertService
from ..utils import logger

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert."""
    try:
        alert = AlertService.create_alert(db, alert_in)
        logger.warning(f"Alert created: {alert.id} - {alert.severity}")
        return alert
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating alert")


@router.get("", response_model=List[AlertResponse])
def list_alerts(
    device_id: Optional[str] = None,
    is_resolved: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List alerts with optional filtering."""
    try:
        if device_id:
            alerts = AlertService.get_alerts_by_device(db, device_id, skip, limit, is_resolved)
        else:
            alerts = AlertService.get_unresolved_alerts(db, skip, limit) if is_resolved is False else []
        return alerts
    except Exception as e:
        logger.error(f"Error listing alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing alerts")


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: str, db: Session = Depends(get_db)):
    """Get a specific alert."""
    alert = AlertService.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    alert_in: AlertUpdate,
    db: Session = Depends(get_db),
):
    """Update an alert."""
    try:
        alert = AlertService.update_alert(db, alert_id, alert_in)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        logger.info(f"Alert updated: {alert_id}")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating alert")


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: str, db: Session = Depends(get_db)):
    """Mark an alert as resolved."""
    try:
        alert = AlertService.resolve_alert(db, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        logger.info(f"Alert resolved: {alert_id}")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Error resolving alert")


@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: str, db: Session = Depends(get_db)):
    """Delete an alert."""
    try:
        success = AlertService.delete_alert(db, alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        logger.info(f"Alert deleted: {alert_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting alert")


@router.get("/stats/count", response_model=dict)
def get_alert_stats(db: Session = Depends(get_db)):
    """Get alert statistics."""
    try:
        total = AlertService.get_alert_count(db)
        unresolved = AlertService.get_alert_count(db, is_resolved=False)
        return {"total": total, "unresolved": unresolved}
    except Exception as e:
        logger.error(f"Error getting alert stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting alert stats")
