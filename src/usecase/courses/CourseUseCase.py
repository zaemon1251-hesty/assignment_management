from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.course import Course
from src.interface.repository.CourseRepository import CourseRepository


class CourseUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    course_repository: CourseRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class CourseUseCase(ABC):
    """course"""
    @abstractmethod
    async def fetch(id: int) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Course) -> List[Course]:
        raise NotImplementedError

    @abstractmethod
    async def add(domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError
