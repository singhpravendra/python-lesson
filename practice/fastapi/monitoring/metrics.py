"""
Prometheus metrics instrumentation for FastAPI.
"""

from prometheus_fastapi_instrumentator import Instrumentator


def setup_metrics(app, *, include_default_handlers: bool = True) -> Instrumentator:
    """
    Configure Prometheus metrics for the FastAPI app.

    Args:
        app: FastAPI application instance.
        include_default_handlers: When True, exposes `/metrics` endpoint.

    Returns:
        Configured Instrumentator instance (can be used for custom metrics).
    """
    instrumentator = Instrumentator(
        excluded_handlers={
            "/metrics",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/health/live",
            "/health/ready",
        },
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_inprogress_requests",
        inprogress_labels=True,
    ).instrument(app)

    if include_default_handlers:
        instrumentator.expose(
            app,
            endpoint="/metrics",
            include_in_schema=False,
        )

    return instrumentator

