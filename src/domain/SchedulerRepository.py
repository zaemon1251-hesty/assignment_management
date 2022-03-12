from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.scheduler import Scheduler


class SchedulerRepository(ABC):
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
    async def update(self, domain: Scheduler) -> Scheduler:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError
