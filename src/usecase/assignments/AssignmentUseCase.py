from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.domain import Assignment, ASSIGNMENT_STATE
from src.domain import Course
from src.domain import AssignmentRepository
from src.domain import SubmissionRepository
from src.domain import TargetAlreadyExsitException, TargetNotFoundException
from src.domain import SUBMISSION_STATE, Submission
from src.usecase.submissions import SubmissionQueryModel, SubmissionService


class AssignmentCommandModel(BaseModel):
    """assignment represents your collection of assignment as an entity."""
    title: str = None
    url: str = None
    info: str = None
    state: int = None
    course_id: int = None
    end_at: datetime = None


class AssignmentUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    assignment_repository: AssignmentRepository
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


class AssignmentUseCase(ABC):
    """Assignment"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Optional[Assignment], course: Optional[Course]) -> List[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: AssignmentCommandModel) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class AssignmentUseCaseImpl(AssignmentUseCase):
    def __init__(
        self,
        uow: AssignmentUseCaseUnitOfWork,
        submission_service: SubmissionService
    ):
        self.uow: AssignmentUseCaseUnitOfWork = uow
        self.submission_service: SubmissionService = submission_service

    async def fetch(self, id: int) -> Optional[Assignment]:
        try:
            assignment = await self.uow.assignment_repository.fetch(id)
            if assignment is None:
                raise TargetNotFoundException("Not Found", Assignment)
        except Exception:
            raise
        return assignment

    async def fetch_all(self, domain: Optional[Assignment]) -> List[Assignment]:
        try:
            assignments = await self.uow.assignment_repository.fetch_all(domain)
        except Exception:
            raise
        return assignments

    async def add(self, domain: Assignment) -> Assignment:
        try:
            exist_assignment = await self.uow.assignment_repository.fetch_by_title(
                domain.title)
            if exist_assignment is not None:
                raise TargetAlreadyExsitException(
                    "title %s already exists" % domain.title, Course)
            assignment = await self.uow.assignment_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return assignment

    async def update(self, id: int, domain: AssignmentCommandModel) -> Assignment:
        try:
            exist = await self.uow.assignment_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Assignment)
            for k, v in domain.dict().items():
                if v:
                    setattr(exist, k, v)
            exist.updated_at = datetime.utcnow()
            assignment = await self.uow.assignment_repository.update(exist)

            # コースの状態変化に合うように、紐づく課題も状態を変化させる
            if domain.state and domain.state != exist.state:
                submission_cond = SubmissionQueryModel(
                    assignment_id=assignment.id)
                correct_submission_state = None
                if domain.state == ASSIGNMENT_STATE.DEAD:
                    submission_cond.state = [
                        SUBMISSION_STATE.NORMAL.value,
                        SUBMISSION_STATE.DANGER.value
                    ]
                    correct_submission_state = SUBMISSION_STATE.EXPIRED
                elif domain.state == ASSIGNMENT_STATE.ALIVE:
                    submission_cond.state = [SUBMISSION_STATE.EXPIRED.value]
                    correct_submission_state = SUBMISSION_STATE.NORMAL
                if correct_submission_state:
                    submissions: List[Submission] = await self.submission_service.fetch_all(
                        submission_cond)
                    for submission in submissions:
                        submission.state = correct_submission_state
                        await self.uow.submission_repository.update(submission)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return assignment

    async def delete(self, id: int) -> bool:
        try:
            exist = self.uow.assignment_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Assignment)
            flg = await self.uow.assignment_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg
