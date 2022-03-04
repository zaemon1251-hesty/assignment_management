from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.scheduler import Scheduler
from src.interface.repository.SchedulerRepository import SchedulerRepository


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
