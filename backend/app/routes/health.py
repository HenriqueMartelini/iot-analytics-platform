"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db

router = APIRouter(tags=["health"])


@router.get("/health", response_model=dict)
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/health/db", response_model=dict)
def health_check_db(db: Session = Depends(get_db)):
    """Database health check endpoint."""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
