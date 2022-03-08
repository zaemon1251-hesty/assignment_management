from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.submission import Submission
from src.domain.user import User
from src.domain.SubmissionRepository import SubmissionRepository


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
