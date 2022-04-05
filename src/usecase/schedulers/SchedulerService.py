from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.scheduler import Scheduler
from .SchedulerModel import SchedulerQueryModel


class SchedulerService(ABC):
    @abstractmethod
    async def fetch_all(self, query: SchedulerQueryModel) -> List[Scheduler]:
        raise NotImplementedError
