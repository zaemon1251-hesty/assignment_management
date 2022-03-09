from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.exception import TargetAlreadyExsitException, TargetNotFoundException
from src.domain.submission import Submission
from src.domain.submission import Submission
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
    async def fetch(self, id: int) -> Optional[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Optional[Submission], submission: Optional[Submission], assignment: Optional[Assignment]) -> List[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class SubmissionUseCaseImpl(SubmissionUseCase):
    def __init__(self, uow: SubmissionUseCaseUnitOfWork):
        self.uow: SubmissionUseCaseUnitOfWork = uow

    async def fetch(self, id: int) -> Optional[Submission]:
        try:
            submission = await self.uow.submission_repository.fetch(id)
            if submission is None:
                raise TargetNotFoundException("Not Found", Submission)
        except Exception:
            raise
        return submission

    async def fetch_all(self, domain: Optional[Submission]) -> List[Submission]:
        try:
            submissions = await self.uow.submission_repository.fetch_all(domain)
        except Exception:
            raise
        return submissions

    async def create(self, domain: Submission) -> Submission:
        try:
            if self.uow.submission_repository.fetch_all(Submission(
                    user_id=domain.user_id, assignment_id=domain.assignment_id)) is not []:
                raise TargetAlreadyExsitException(
                    "target alraedy exists", Submission)

            submission = await self.uow.submission_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return submission

    async def update(self, id: int, domain: Submission) -> Submission:
        try:
            if self.uow.submission_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Submission)
            submission = await self.uow.submission_repository.update(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return submission

    async def delete(self, id: int) -> bool:
        try:
            if self.uow.submission_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Submission)
            flg = await self.uow.submission_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg
