"""
Main application entry point for the IoT Analytics Platform.

This module initializes the FastAPI application, configures middleware,
registers routes, and sets up database initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config import get_settings
from .database import engine
from .models import Base
from .routes import devices_router, sensor_readings_router, alerts_router, health_router
from .utils import logger

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="IoT Analytics API",
    description="Real-time data analytics platform for IoT devices",
    version="1.0.0",
)

settings = get_settings()

# Add middleware for security and CORS
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API route modules
app.include_router(health_router)
app.include_router(devices_router)
app.include_router(sensor_readings_router)
app.include_router(alerts_router)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Application started")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Application shutdown")


@app.get("/")
def root():
    """Root endpoint returning API information."""
    return {
        "message": "IoT Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
