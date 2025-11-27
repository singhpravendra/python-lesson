"""
User service layer for business logic.
"""

import logging
from typing import Optional

from entities.user_entity import UserEntity
from utils.id_generator import generate_id
from repositories.base_user_repo import BaseUserRepository
from exceptions.custom_exceptions import NotFoundError, ConflictError, ValidationError

logger = logging.getLogger(__name__)


class UserService:
    """Service for user business logic operations."""

    def __init__(self, repo: BaseUserRepository):
        self.repo = repo

    async def create(self, name: str, email: str) -> UserEntity:
        """
        Create a new user.
        
        Args:
            name: User's name
            email: User's email address
            
        Returns:
            Created UserEntity
            
        Raises:
            ConflictError: If email already exists
            ValidationError: If input validation fails
        """
        # Validate email format (basic check)
        if not email or "@" not in email:
            raise ValidationError("Invalid email format", field="email")
        
        # Check for duplicate email
        existing_users = await self.repo.list()
        if any(user.email.lower() == email.lower() for user in existing_users):
            raise ConflictError(f"User with email '{email}' already exists")
        
        user = UserEntity(
            id=generate_id(),
            name=name.strip(),
            email=email.lower().strip()
        )
        
        saved_user = await self.repo.save(user)
        logger.info(f"Created user: {saved_user.id} ({saved_user.email})")
        
        return saved_user

    async def get(self, user_id: str) -> Optional[UserEntity]:
        """
        Get a user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserEntity if found, None otherwise
        """
        if not user_id:
            raise ValidationError("User ID is required", field="user_id")
        
        user = await self.repo.find(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        return user

    async def list(self) -> list[UserEntity]:
        """
        List all users.
        
        Returns:
            List of UserEntity objects
        """
        users = await self.repo.list()
        logger.debug(f"Retrieved {len(users)} users")
        return users

    async def delete(self, user_id: str) -> None:
        """
        Delete a user by ID.
        
        Args:
            user_id: User identifier
            
        Raises:
            NotFoundError: If user doesn't exist
        """
        if not user_id:
            raise ValidationError("User ID is required", field="user_id")
        
        user = await self.repo.find(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        await self.repo.delete(user_id)
        logger.info(f"Deleted user: {user_id}")

