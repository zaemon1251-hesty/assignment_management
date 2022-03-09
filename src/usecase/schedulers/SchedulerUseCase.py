from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.exception import TargetNotFoundException

from src.domain.scheduler import Scheduler
from src.domain.SchedulerRepository import SchedulerRepository


class SchedulerUseCaseUnitOfWork(ABC):
    """UseCaseUnitOfWork defines an interface based on Unit of Work pattern."""
    scheduler_repository = SchedulerRepository

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
    async def fetch(id: int) -> Optional[Scheduler]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Scheduler) -> List[Scheduler]:
        raise NotImplementedError

    @abstractmethod
    async def add(domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def deadline_reminder() -> bool:
        raise NotImplementedError


class SchedulerUseCaseImpl(SchedulerUseCase):
    def __init__(self, uow: SchedulerUseCaseUnitOfWork):
        self.uow: SchedulerUseCaseUnitOfWork = uow

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
