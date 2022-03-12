from abc import ABC, abstractmethod
from typing import List, Optional

from domain.user import User, AuthedUser


class UserRepository(ABC):
    """UserRepository a query usecase inteface related User entity."""

    @abstractmethod
    async def fetch(id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_name(name: str = None) -> Optional[AuthedUser]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Optional[User]) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(domain: AuthedUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: AuthedUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError
