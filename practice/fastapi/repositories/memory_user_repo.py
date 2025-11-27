"""
In-memory user repository implementation.
For production, replace with a database-backed repository.
"""

from typing import Optional
from entities.user_entity import UserEntity
from repositories.base_user_repo import BaseUserRepository


class InMemoryUserRepo(BaseUserRepository):
    """In-memory implementation of user repository."""
    
    # Class-level storage (shared across instances)
    storage: dict[str, UserEntity] = {}

    async def save(self, user: UserEntity) -> UserEntity:
        """
        Save a user entity.
        
        Args:
            user: UserEntity to save
            
        Returns:
            Saved UserEntity
        """
        self.storage[user.id] = user
        return user

    async def find(self, user_id: str) -> Optional[UserEntity]:
        """
        Find a user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserEntity if found, None otherwise
        """
        return self.storage.get(user_id)

    async def list(self) -> list[UserEntity]:
        """
        List all users.
        
        Returns:
            List of all UserEntity objects
        """
        return list(self.storage.values())

    async def delete(self, user_id: str) -> None:
        """
        Delete a user by ID.
        
        Args:
            user_id: User identifier
        """
        self.storage.pop(user_id, None)
    
    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Find a user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            UserEntity if found, None otherwise
        """
        email_lower = email.lower()
        for user in self.storage.values():
            if user.email.lower() == email_lower:
                return user
        return None

