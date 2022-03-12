from abc import ABC, abstractmethod
from typing import List, Optional

from domain.assignment import Assignment
from domain.course import Course


class AssignmentRepository(ABC):
    """Assignment"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_title(self, title: str) -> Optional[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Optional[Assignment], course: Optional[Course]) -> List[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain: Assignment) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> Assignment:
        raise NotImplementedError
