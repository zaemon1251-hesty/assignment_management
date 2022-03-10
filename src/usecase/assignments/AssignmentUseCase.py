from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.assignment import Assignment, ASSIGNMENT_STATE
from src.domain.course import Course
from src.domain.AssignmentRepository import AssignmentRepository
from src.domain.exception import TargetAlreadyExsitException, TargetNotFoundException


class AssignmentUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    assignment_repository: AssignmentRepository

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
    async def update(self, id: int, domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class AssignmentUseCaseImpl(AssignmentUseCase):
    def __init__(self, uow: AssignmentUseCaseUnitOfWork):
        self.uow: AssignmentUseCaseUnitOfWork = uow

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

    async def create(self, domain: Assignment) -> Assignment:
        try:
            if self.uow.assignment_repository.fetch_by_title(
                    domain.title) is not None:
                raise TargetAlreadyExsitException(
                    "title %s already exists" % domain.title, Course)
            assignment = await self.uow.assignment_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return assignment

    async def update(self, id: int, domain: Assignment) -> Assignment:
        try:
            if self.uow.assignment_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Assignment)
            domain.updated_at = datetime.utcnow()
            assignment = await self.uow.assignment_repository.update(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return assignment

    async def delete(self, id: int) -> bool:
        try:
            if self.uow.assignment_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Assignment)
            flg = await self.uow.assignment_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg
