"""
User entity representing the domain model.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    """User domain entity."""
    
    id: str
    name: str
    email: str
    created_at: datetime | None = None
    
    def __post_init__(self):
        """Set created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()

