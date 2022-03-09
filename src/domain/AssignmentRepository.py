from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.course import Course


class AssignmentRepository(ABC):
    """Assignment"""
    @abstractmethod
    async def fetch(id: int) -> Optional[Assignment]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_title(title: str) -> Optional[Assignment]:
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
    async def delete(id: int) -> Assignment:
        raise NotImplementedError
