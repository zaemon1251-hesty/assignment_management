from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.AssignmentRepository import AssignmentRepository
from src.domain.UserRepository import UserRepository
from src.domain.assignment import Assignment
from src.domain.submission import Submission
from src.domain.exception import TargetNotFoundException
from src.domain.scheduler import Scheduler
from src.domain.SchedulerRepository import SchedulerRepository
from src.domain.user import User
from src.usecase.driver.NotifyDriver import NotifyDriver


class SchedulerUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    scheduler_repository: SchedulerRepository
    assignment_repository: AssignmentRepository
    user_repository: UserRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SchedulerUseCase(ABC):
    """submission"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Scheduler]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Scheduler) -> List[Scheduler]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def deadline_reminder(self) -> bool:
        raise NotImplementedError


class SchedulerUseCaseImpl(SchedulerUseCase):
    def __init__(self, uow: SchedulerUseCaseUnitOfWork, driver: NotifyDriver):
        self.uow: SchedulerUseCaseUnitOfWork = uow
        self.driver: NotifyDriver = driver

    async def fetch(self, id: int) -> Optional[Scheduler]:
        try:
            scheduler = await self.uow.scheduler_repository.fetch(id)
            if scheduler is None:
                raise TargetNotFoundException("Not Found", Scheduler)
        except Exception:
            raise
        return scheduler

    async def fetch_all(self, domain: Optional[Scheduler]) -> List[Scheduler]:
        try:
            schedulers = await self.uow.scheduler_repository.fetch_all(domain)
        except Exception:
            raise
        return schedulers

    async def create(self, domain: Scheduler) -> Scheduler:
        try:
            scheduler = await self.uow.scheduler_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return scheduler

    async def update(self, id: int, domain: Scheduler) -> Scheduler:
        try:
            if self.uow.scheduler_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Scheduler)
            scheduler = await self.uow.scheduler_repository.update(domain)
            if scheduler is None:
                raise TargetNotFoundException("Not Found", Scheduler)
            domain.updated_at = datetime.utcnow()
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return scheduler

    async def delete(self, id: int) -> bool:
        try:
            if self.uow.scheduler_repository.fetch(id) is None:
                raise TargetNotFoundException("Not Found", Scheduler)
            flg = await self.uow.scheduler_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg

    async def deadline_reminder(self) -> bool:
        active_scheduler = Scheduler(
            remind_at=datetime.utcnow().timestamp(),
            reminded=False
        )
        schedules: List[Scheduler] = await self.uow.scheduler_repository.fetch_all(active_scheduler)
        try:
            self.uow.begin()
            for schedule in schedules:
                if schedule.submission is None:
                    raise TargetNotFoundException()
                assignment: Assignment = schedule.submission.assignment
                if assignment is None:
                    assignment = self.uow.assignment_repository.fetch(
                        schedule.submission.assignment_id)
                user: User = schedule.submission.user
                if user is None:
                    user = self.uow.user_repository.fetch(
                        schedule.submission.user_id)
                self.driver.notify(
                    user,
                    assignment,
                    schedule.submission.state
                )
                schedule.reminded = True
                self.uow.scheduler_repository.update(schedule)
            self.uow.commit()
        except TargetNotFoundException as e:
            pass
        except Exception as e:
            self.uow.rollback()
            raise
        return True
