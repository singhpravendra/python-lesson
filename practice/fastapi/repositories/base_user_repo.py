from abc import ABC, abstractmethod
from entities.user_entity import UserEntity

class BaseUserRepository(ABC):

    @abstractmethod
    async def save(self, user: UserEntity): pass

    @abstractmethod
    async def find(self, user_id: str) -> UserEntity | None: pass

    @abstractmethod
    async def list(self) -> list[UserEntity]: pass

    @abstractmethod
    async def delete(self, user_id: str): pass
