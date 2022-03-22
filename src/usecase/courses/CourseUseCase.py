from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain import AssignmentRepository
from src.domain import Course
from src.domain import Assignment
from src.domain import Course
from src.domain import CourseRepository
from src.domain import TargetAlreadyExsitException, TargetNotFoundException
from src.usecase.assignments import AssignmentUseCase
from src.usecase.driver import ScrapeDriver


class CourseUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    course_repository: CourseRepository
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


class CourseUseCase(ABC):
    """course"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Course) -> List[Course]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: Course) -> Course:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def periodically_scraper(self, keywords: List[str]) -> bool:
        raise NotImplementedError


class CourseUseCaseImpl(CourseUseCase):
    def __init__(self, uow: CourseUseCaseUnitOfWork, driver: ScrapeDriver):
        self.uow: CourseUseCaseUnitOfWork = uow
        self.driver: ScrapeDriver = driver

    async def fetch(self, id: int) -> Optional[Course]:
        try:
            course = await self.uow.course_repository.fetch(id)
            if course is None:
                raise TargetNotFoundException("Not Found", Course)
        except Exception:
            raise
        return course

    async def fetch_all(self, domain: Optional[Course]) -> List[Course]:
        try:
            courses = await self.uow.course_repository.fetch_all(domain)
        except Exception:
            raise
        return courses

    async def add(self, domain: Course) -> Course:
        try:
            exist_course = await self.uow.course_repository.fetch_by_title(
                domain.title)
            if exist_course is not None:
                raise TargetAlreadyExsitException(
                    "title %s already exists" % domain.title, Course)
            course = await self.uow.course_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return course

    async def update(self, id: int, domain: Course) -> Course:
        try:
            exist = self.uow.course_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Course)
            domain.updated_at = datetime.utcnow()
            course = await self.uow.course_repository.update(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return course

    async def delete(self, id: int) -> bool:
        try:
            exist = self.uow.course_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Course)
            flg = await self.uow.course_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg

    async def periodically_scraper(self, keywords: List[str]) -> bool:
        assignments, courses = await self.driver.run(keywords)
        try:
            self.uow.begin()
            for course in courses:
                course_ex = await self.uow.course_repository.fetch(course.id)
                if course_ex:
                    await self.uow.course_repository.update(course)
                else:
                    await self.uow.course_repository.add(course)
            self.uow.commit()

            self.uow.begin()
            for assignment in assignments:
                assignment_ex = await self.uow.assignment_repository.fetch(
                    assignment.id)
                if assignment_ex:
                    await self.uow.course_repository.update(course)
                else:
                    await self.uow.assignment_repository.add(assignment)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            return False
        return True
