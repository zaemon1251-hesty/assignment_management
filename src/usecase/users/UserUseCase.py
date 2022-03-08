from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.user import User, AuthedUser
from src.domain.UserRepository import UserRepository
from src.usecase.token import Token


class UserUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    user_repository: UserRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class UserUseCase(ABC):
    """UserUseCase defines a query usecase inteface related User entity."""

    @abstractmethod
    async def fetch(id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_token(token: str) -> AuthedUser:
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
    async def auth_verify(token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_token(name: str, password: str) -> Token:
        raise NotImplementedError
