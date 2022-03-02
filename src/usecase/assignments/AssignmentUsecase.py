from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignments.AssignmentModel import Assignment
from src.domain.assignments.AssignmentState import assignment_state
from src.domain.courses.CourseModel import Course


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
    async def change_status(id: int, state: assignment_state) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError
