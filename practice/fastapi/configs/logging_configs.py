"""
Logging configuration for the application.
"""

import logging
import sys
from configs.context import get_trace_id
from settings.config import settings


class ContextFilter(logging.Filter):
    """Logging filter to add context information to log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add trace ID and other context to log record."""
        record.trace_id = get_trace_id()
        record.service = settings.service_name
        record.env = settings.env
        
        # Optional extras that can be populated by middleware:
        record.method = getattr(record, "method", "-")
        record.path = getattr(record, "path", "-")
        record.status = getattr(record, "status", "-")
        record.duration_ms = getattr(record, "duration_ms", "-")
        record.client_ip = getattr(record, "client_ip", "-")
        
        return True


def get_log_format() -> str:
    """Get log format based on configuration."""
    if settings.log_format == "json":
        # JSON format for structured logging (production)
        return (
            '{"timestamp": "%(asctime)s", '
            '"level": "%(levelname)s", '
            '"service": "%(service)s", '
            '"env": "%(env)s", '
            '"logger": "%(name)s", '
            '"trace_id": "%(trace_id)s", '
            '"message": "%(message)s", '
            '"module": "%(module)s", '
            '"function": "%(funcName)s", '
            '"line": %(lineno)d}'
        )
    else:
        # Human-readable format (development)
        return (
            "%(asctime)s [%(levelname)s] "
            "%(service)s [%(env)s] "
            "%(name)s [%(trace_id)s] "
            "%(message)s"
        )


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "context": {
            "()": ContextFilter
        }
    },
    "formatters": {
        "default": {
            "format": get_log_format(),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": (
                "%(asctime)s [%(levelname)s] "
                "%(service)s [%(env)s] "
                "%(name)s [%(trace_id)s] "
                "[%(method)s %(path)s %(status)s %(duration_ms)sms] "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["context"],
            "stream": sys.stdout
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "filters": ["context"],
            "stream": sys.stderr,
            "level": "ERROR"
        }
    },
    "loggers": {
        "": {  # Root logger
            "level": settings.log_level,
            "handlers": ["console", "error_console"],
            "propagate": False
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": "INFO" if settings.is_development else "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": False
        }
    }
}
