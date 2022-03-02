from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.schedulers.SchedulerModel import Scheduler
from src.domain.submissions.SubmissionModel import Submission


class SchedulerRepository(ABC):
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
