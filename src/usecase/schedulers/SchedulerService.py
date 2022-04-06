from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.scheduler import Scheduler
from .SchedulerModel import SchedulerQueryModel


class SchedulerService(ABC):
    @abstractmethod
    async def fetch_all(self, query: SchedulerQueryModel) -> List[Scheduler]:
        raise NotImplementedError
