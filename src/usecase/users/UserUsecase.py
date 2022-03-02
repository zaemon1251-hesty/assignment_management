from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.users.UserModel import User


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
    async def delete(id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def login(name: str, password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def periodically_scraper(superuser: User) -> bool:
        raise NotImplementedError
