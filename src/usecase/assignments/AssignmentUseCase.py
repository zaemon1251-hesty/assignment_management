from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.AssignmentState import ASSIGNMENT_STATE
from src.domain.course import Course
from src.interface.repository.AssignmentRepository import AssignmentRepository


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
    async def fetch(id: int) -> Optional[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Optional[Assignment], course: Optional[Course]) -> List[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def add(domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def change_status(id: int, state: ASSIGNMENT_STATE) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError
