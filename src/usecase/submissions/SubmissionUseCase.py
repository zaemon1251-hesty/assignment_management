from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.domain.assignment import Assignment
from src.domain.exception import TargetAlreadyExsitException, TargetNotFoundException
from src.domain import Submission, SubmissionRepository, SUBMISSION_STATE
from .SubmissionService import SubmissionQueryModel, SubmissionService


class SubmissionCommandModel(BaseModel):
    """submission represents your registerd assignment as an entity."""

    user_id: int = None
    assignment_id: int = None
    state: int = None


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
    async def fetch_all(self, domain: Optional[SubmissionQueryModel]) -> List[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: SubmissionCommandModel) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class SubmissionUseCaseImpl(SubmissionUseCase):
    def __init__(
        self,
        uow: SubmissionUseCaseUnitOfWork,
        service: SubmissionService
    ):
        self.uow: SubmissionUseCaseUnitOfWork = uow
        self.service: SubmissionService = service

    async def fetch(self, id: int) -> Optional[Submission]:
        try:
            submission = await self.uow.submission_repository.fetch(id)
            if submission is None:
                raise TargetNotFoundException("Not Found", Submission)
        except Exception:
            raise
        return submission

    async def fetch_all(self, domain: Optional[SubmissionQueryModel]) -> List[Submission]:
        try:
            submissions = await self.service.fetch_all(domain)
        except Exception:
            raise
        return submissions

    async def add(self, domain: Submission) -> Submission:
        try:
            exist_submission = await self.uow.submission_repository.fetch_all(Submission(
                user_id=domain.user_id, assignment_id=domain.assignment_id))
            if exist_submission != []:
                raise TargetAlreadyExsitException(
                    "target alraedy exists", Submission)

            submission = await self.uow.submission_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return submission

    async def update(self, id: int, domain: SubmissionCommandModel) -> Submission:
        try:
            exist = await self.uow.submission_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Submission)
            for k, v in domain.dict().items():
                if v:
                    setattr(exist, k, v)
            exist.updated_at = datetime.utcnow()
            submission = await self.uow.submission_repository.update(exist)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return submission

    async def delete(self, id: int) -> bool:
        try:
            exist = await self.uow.submission_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Submission)
            flg = await self.uow.submission_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg
