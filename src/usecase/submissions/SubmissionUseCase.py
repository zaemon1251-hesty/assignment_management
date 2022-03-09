from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.exception import TargetNotFoundException
from src.domain.submission import Submission
from src.domain.user import User
from src.domain.SubmissionRepository import SubmissionRepository
from src.settings import logger


class SubmissionUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    submission_repository: SubmissionRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SubmissionUseCase(ABC):
    """submission"""
    @abstractmethod
    async def fetch(id: int) -> Optional[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Optional[Submission], user: Optional[User], assignment: Optional[Assignment]) -> List[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def add(domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def scraping_add(user: User) -> bool:
        raise NotImplementedError


class UserUseCaseImpl(SubmissionUseCase):
    def __init__(self, uow: SubmissionUseCaseUnitOfWork, driver=AuthDriver):
        self.uow: SubmissionUseCaseUnitOfWork = uow
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

    async def create(self, domain: Submission) -> User:
        try:
            if domain.password is not None:
                domain.password = self.driver.get_password_hash(
                    domain.password)
            user = await self.uow.user_repository.create(domain)
            if user is None:
                raise TargetNotFoundException("Not Found", User)
        except Exception as e:
            logger.error(e)
            raise
        return user

    async def update(self, domain: Submission) -> User:
        try:
            if domain.password is not None:
                domain.password = self.driver.get_password_hash(
                    domain.password)
            user = await self.uow.user_repository.update(domain)
            if user is None:
                raise TargetNotFoundException("Not Found", User)
        except Exception as e:
            logger.error(e)
            raise
        return user

    async def delete(self, id: int) -> bool:
        try:
            flg = await self.uow.user_repository.delete(id)
        except Exception as e:
            logger.error(e)
            raise
        return flg
