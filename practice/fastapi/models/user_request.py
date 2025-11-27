"""
Request models for user operations.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateRequest(BaseModel):
    """Request model for creating a new user."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name",
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["john.doe@example.com"]
    )
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and sanitize name."""
        name = v.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return name
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }


class UserUpdateRequest(BaseModel):
    """Request model for updating a user."""
    
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="User's full name"
    )
    email: EmailStr | None = Field(
        None,
        description="User's email address"
    )
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Validate name if provided."""
        if v is not None:
            name = v.strip()
            if not name:
                raise ValueError("Name cannot be empty")
            if len(name) < 2:
                raise ValueError("Name must be at least 2 characters long")
            return name
        return v

