"""
User API routes.
"""

import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from models.user_request import UserCreateRequest, UserUpdateRequest
from models.user_response import UserResponse, UserListResponse
from services.user_service import UserService
from repositories.memory_user_repo import InMemoryUserRepo
from configs.context import get_trace_id

router = APIRouter()
logger = logging.getLogger(__name__)


def get_user_service() -> UserService:
    """
    Dependency to get UserService instance.
    In production, use dependency injection container.
    """
    repo = InMemoryUserRepo()
    return UserService(repo)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with name and email. Email must be unique."
)
async def create_user(
    payload: UserCreateRequest,
    svc: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    """
    Create a new user.
    
    - **name**: User's full name (1-100 characters)
    - **email**: User's email address (must be unique)
    
    Returns the created user with generated ID and trace ID.
    """
    user = await svc.create(payload.name, payload.email)
    logger.info(f"Created user: {user.id} ({user.email})")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        trace_id=get_trace_id()
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier."
)
async def get_user(
    user_id: Annotated[str, Path(..., description="User identifier")],
    svc: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    """
    Get a user by ID.
    
    - **user_id**: Unique user identifier (UUID)
    
    Returns user details or 404 if not found.
    """
    user = await svc.get(user_id)
    logger.info(f"Retrieved user: {user_id}")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        trace_id=get_trace_id()
    )


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List all users",
    description="Retrieve a list of all users in the system."
)
async def list_users(
    svc: Annotated[UserService, Depends(get_user_service)]
) -> UserListResponse:
    """
    List all users.
    
    Returns a list of all users with pagination metadata.
    """
    users = await svc.list()
    logger.info(f"Listed {len(users)} users")
    
    trace_id = get_trace_id()
    user_responses = [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            created_at=u.created_at,
            trace_id=trace_id
        )
        for u in users
    ]
    
    return UserListResponse(
        users=user_responses,
        total=len(user_responses),
        trace_id=trace_id
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by their unique identifier."
)
async def delete_user(
    user_id: Annotated[str, Path(..., description="User identifier")],
    svc: Annotated[UserService, Depends(get_user_service)]
) -> None:
    """
    Delete a user by ID.
    
    - **user_id**: Unique user identifier (UUID)
    
    Returns 204 No Content on success, 404 if not found.
    """
    await svc.delete(user_id)
    logger.info(f"Deleted user: {user_id}")
    return None
