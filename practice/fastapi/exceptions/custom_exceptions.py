"""
Custom exception classes for the application.
"""

from typing import Any, Optional


class AppException(Exception):
    """Base exception for all application exceptions."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, identifier: str, details: Optional[dict] = None):
        message = f"{resource} with id '{identifier}' not found"
        super().__init__(message, status_code=404, details=details)


class ValidationError(AppException):
    """Validation error exception."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[dict] = None):
        if field:
            message = f"Validation error in field '{field}': {message}"
        super().__init__(message, status_code=422, details=details)


class ConflictError(AppException):
    """Resource conflict exception (e.g., duplicate entry)."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=409, details=details)


class UnauthorizedError(AppException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized", details: Optional[dict] = None):
        super().__init__(message, status_code=401, details=details)


class ForbiddenError(AppException):
    """Forbidden access exception."""
    
    def __init__(self, message: str = "Forbidden", details: Optional[dict] = None):
        super().__init__(message, status_code=403, details=details)

