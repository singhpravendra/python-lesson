"""
Production-grade FastAPI application entry point.
"""

import logging.config
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from middleware.request_context import RequestContextMiddleware
from configs.logging_configs import LOGGING_CONFIG
from apis.routes import health, users
from settings.config import settings
from exceptions.handlers import setup_exception_handlers
from monitoring.metrics import setup_metrics

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Handles startup and shutdown logic.
    """
    # Startup
    logger.info(
        f"Starting {settings.service_name} in {settings.env} environment",
        extra={
            "service": settings.service_name,
            "env": settings.env,
            "port": settings.port,
            "host": settings.host
        }
    )
    
    if settings.is_development:
        logger.warning("Running in DEVELOPMENT mode - not suitable for production")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.service_name}")


def create_fastapi_app() -> FastAPI:
    """
    Create and configure FastAPI application instance.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.service_name,
        description="Production-grade user management API built with FastAPI",
        version="1.0.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add request context middleware (must be last)
    app.add_middleware(RequestContextMiddleware)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include routers
    app.include_router(
        health.router,
        prefix=settings.api_prefix,
        tags=["Health"]
    )
    app.include_router(
        users.router,
        prefix=f"{settings.api_prefix}/users",
        tags=["Users"]
    )
    
    # Setup metrics instrumentation (exposes /metrics)
    setup_metrics(app)

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "service": settings.service_name,
            "version": "1.0.0",
            "status": "running",
            "environment": settings.env,
            "docs": "/docs" if not settings.is_production else "disabled in production"
        }
    
    return app


def main():
    """
    Main application entry point.
    """
    try:
        app = create_fastapi_app()
        
        import uvicorn
        server_url = f"http://{settings.host}:{settings.port}"
        docs_url = f"{server_url}/docs" if not settings.is_production else "disabled in production"

        logger.info(
            f"Starting {settings.service_name} on {settings.host}:{settings.port}",
            extra={
                "service": settings.service_name,
                "env": settings.env,
                "host": settings.host,
                "port": settings.port,
                "url": server_url,
                "docs": docs_url
            }
        )

        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            access_log=True,
            log_level=settings.log_level.lower(),
            reload=settings.is_development and settings.debug,
        )
        logger.info(
            "FastAPI server stopped",
            extra={
                "service": settings.service_name,
                "env": settings.env,
                "host": settings.host,
                "port": settings.port
            }
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
