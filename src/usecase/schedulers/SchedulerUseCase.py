from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

from src.domain import SubmissionRepository, ASSIGNMENT_STATE, SUBMISSION_STATE

from src.domain.UserRepository import UserRepository
from src.domain import Assignment
from src.domain import Submission
from src.domain import TargetNotFoundException
from src.domain import Scheduler
from src.domain import SchedulerRepository
from src.domain import User
from src.usecase.driver.NotifyDriver import NotifyDriver
from src.usecase.assignments import AssignmentQueryModel
from src.usecase.submissions import SubmissionQueryModel, SubmissionService
from .SchedulerService import SchedulerQueryModel, SchedulerService
from .SchedulerModel import SchedulerCommandModel


class SchedulerUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    scheduler_repository: SchedulerRepository
    submission_repository: SubmissionRepository
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
    async def fetch_all(self, domain: SchedulerQueryModel) -> List[Scheduler]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, domain: SchedulerCommandModel) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def deadline_reminder(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_remind_schedule(self, by: timedelta) -> List[Scheduler]:
        raise NotImplementedError


class SchedulerUseCaseImpl(SchedulerUseCase):
    def __init__(
            self,
            uow: SchedulerUseCaseUnitOfWork,
            service: SchedulerService,
            submission_service: SubmissionService,
            driver: NotifyDriver):
        self.uow: SchedulerUseCaseUnitOfWork = uow
        self.driver: NotifyDriver = driver
        self.service: SchedulerService = service
        self.submission_service: SubmissionService = submission_service

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
            schedulers = await self.service.fetch_all(domain)
        except Exception:
            raise
        return schedulers

    async def add(self, domain: Scheduler) -> Scheduler:
        try:
            scheduler = await self.uow.scheduler_repository.add(domain)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return scheduler

    async def update(self, id: int, domain: SchedulerCommandModel) -> Scheduler:
        try:
            exist = await self.uow.scheduler_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Scheduler)
            for k, v in domain.dict().items():
                if v:
                    setattr(exist, k, v)
            scheduler = await self.uow.scheduler_repository.update(exist)
            exist.updated_at = datetime.utcnow()
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return scheduler

    async def delete(self, id: int) -> bool:
        try:
            exist = await self.uow.scheduler_repository.fetch(id)
            if exist is None:
                raise TargetNotFoundException("Not Found", Scheduler)
            flg = await self.uow.scheduler_repository.delete(id)
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise
        return flg

    async def deadline_reminder(self) -> bool:
        """リマインドの実行"""
        active_scheduler = SchedulerQueryModel(
            remind_be=datetime.utcnow().timestamp(),
            reminded=False
        )
        schedules: List[Scheduler] = await self.service.fetch_all(active_scheduler)
        try:
            for schedule in schedules:
                schedule.submission = await self.uow.submission_repository.fetch(schedule.submission_id)
                user = await self.uow.user_repository.fetch(schedule.submission.user_id)
                flg = await self.driver.notify(
                    user,
                    schedule.submission.assignment,
                    schedule.submission.state
                )
                schedule.reminded = True
                await self.uow.scheduler_repository.update(schedule)
            self.uow.commit()
        except TargetNotFoundException as e:
            pass
        except Exception as e:
            self.uow.rollback()
            raise
        return True

    async def add_remind_schedule(self, by: timedelta = timedelta(days=3)) -> List[Scheduler]:
        new_scs: List[Scheduler] = []

        query = SubmissionQueryModel(
            state=[SUBMISSION_STATE.NORMAL],
            assignment=AssignmentQueryModel(
                state=[ASSIGNMENT_STATE.ALIVE],
                end_be=datetime.utcnow() + by
            )
        )
        submissions = await self.submission_service.fetch_all(query)
        try:
            for submission in submissions:
                exist = await self.uow.scheduler_repository.fetch(submission.id)
                if exist is not None:
                    continue

                schedule = Scheduler(
                    submission_id=submission.id,
                    remind_at=datetime.utcnow(),
                    reminded=False
                )

                new_sc = await self.uow.scheduler_repository.update(schedule)
                new_scs.append(new_sc)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
        return new_scs
