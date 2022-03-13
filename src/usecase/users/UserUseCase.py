from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from src.domain.exception import TargetAlreadyExsitException, TargetNotFoundException

from src.domain.user import User, AuthedUser
from src.domain.UserRepository import UserRepository
from src.usecase.driver.AuthDriver import AuthDriver
from src.usecase.token import Token


class UserCommandModel(User):
    password: str = None


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
    async def fetch(self, id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_token(self, token: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Optional[User]) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, domain: UserCommandModel) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: UserCommandModel) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def auth_verify(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_token(self, name: str, password: str) -> Token:
        raise NotImplementedError


class UserUseCaseImpl(UserUseCase):
    def __init__(self, uow: UserUseCaseUnitOfWork, driver: AuthDriver):
        self.uow: UserUseCaseUnitOfWork = uow
        self.driver = driver

    async def fetch(self, id: int) -> Optional[User]:
        try:
            user = await self.uow.user_repository.fetch(id)
            if user is None:
                raise TargetNotFoundException("Not Found", User)
        except Exception:
            raise
        return user

    async def fetch_all(self, domain: Optional[User]) -> List[User]:
        try:
            users = await self.uow.user_repository.fetch_all(domain)
        except Exception:
            raise
        return users

    async def create(self, domain: UserCommandModel) -> User:
        try:
            if self.uow.user_repository.fetch_by_name(domain.name) is not None:
                raise TargetAlreadyExsitException(
                    "name %s alraedy exists" % domain.name, User)
            if domain.password is not None:
                domain.password = self.driver.get_password_hash(
                    domain.password)
            domain: AuthedUser = AuthedUser(**dict(domain))
            user = await self.uow.user_repository.create(domain)
            if user is None:
                raise TargetNotFoundException("Not Found", User)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return user

    async def update(self, id: int, domain: UserCommandModel) -> User:
        try:
            if self.uow.user_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", User)
            if domain.password is not None:
                domain.password = self.driver.get_password_hash(
                    domain.password)
            domain: AuthedUser = AuthedUser(**dict(domain))
            domain.updated_at = datetime.utcnow()
            user = await self.uow.user_repository.update(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return user

    async def delete(self, id: int) -> bool:
        try:
            if self.uow.user_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", User)

            flg = await self.uow.user_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg

    async def fetch_by_token(self, token: str) -> User:
        try:
            user = await self.driver.get_user_by_token(token)
            if user is None:
                raise TargetNotFoundException("Not Found", User)
        except Exception:
            raise
        return user

    def auth_verify(self, token: str) -> bool:
        flg = self.driver.authenticate_token(token)
        return True if flg is not None else False

    def create_token(self, name: str, password: str) -> Token:
        token: Token = self.driver.create_access_token(name, password)
        return token
