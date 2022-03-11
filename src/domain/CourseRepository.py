from abc import ABC, abstractmethod
from typing import List, Optional

from domain.course import Course


class CourseRepository(ABC):
    """submission"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_title(self, title: str) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Course) -> List[Course]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError
