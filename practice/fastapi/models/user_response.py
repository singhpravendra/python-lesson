"""
Response models for user operations.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserResponse(BaseModel):
    """Response model for user data."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2024-01-15T10:30:00Z",
                "trace_id": "abc123"
            }
        }
    )
    
    id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime | None = Field(None, description="User creation timestamp")
    trace_id: str = Field(..., description="Request trace ID")


class UserListResponse(BaseModel):
    """Response model for user list with pagination."""
    
    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    trace_id: str = Field(..., description="Request trace ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "created_at": "2024-01-15T10:30:00Z",
                        "trace_id": "abc123"
                    }
                ],
                "total": 1,
                "trace_id": "abc123"
            }
        }
    )

