from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.courses.CourseModel import Course
from src.interface.driver.FetchDriver import crude_course


class CourseRepository(ABC):
    """submission"""
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
    async def delete(id: int) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def commit_by_scrape(data: crude_course) -> Course:
        raise NotImplementedError
