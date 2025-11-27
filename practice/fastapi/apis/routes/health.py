"""
Health check endpoints.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from settings.config import settings
from configs.context import get_trace_id

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/health",
    summary="Health check",
    description="Basic health check endpoint to verify service is running.",
    tags=["Health"]
)
async def health() -> JSONResponse:
    """
    Basic health check endpoint.
    
    Returns service status and basic information.
    """
    logger.debug("Health check requested")
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": settings.service_name,
            "environment": settings.env,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": get_trace_id()
        }
    )


@router.get(
    "/health/ready",
    summary="Readiness check",
    description="Readiness probe for Kubernetes/container orchestration.",
    tags=["Health"]
)
async def readiness() -> JSONResponse:
    """
    Readiness check endpoint.
    
    Use this endpoint to verify the service is ready to accept traffic.
    In production, add checks for database connectivity, external services, etc.
    """
    # TODO: Add actual readiness checks (database, cache, etc.)
    is_ready = True
    
    if not is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "service": settings.service_name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "trace_id": get_trace_id()
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "ready",
            "service": settings.service_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": get_trace_id()
        }
    )


@router.get(
    "/health/live",
    summary="Liveness check",
    description="Liveness probe for Kubernetes/container orchestration.",
    tags=["Health"]
)
async def liveness() -> JSONResponse:
    """
    Liveness check endpoint.
    
    Use this endpoint to verify the service is alive.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "alive",
            "service": settings.service_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": get_trace_id()
        }
    )
