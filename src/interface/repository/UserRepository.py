from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.user import User


class UserUsecase(ABC):
    """UserUseCase defines a query usecase inteface related User entity."""

    @abstractmethod
    async def fetch(id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_name(name: Optional[str] = None) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Optional[User]) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(domain: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def deadline_reminder() -> bool:
        raise NotImplementedError
