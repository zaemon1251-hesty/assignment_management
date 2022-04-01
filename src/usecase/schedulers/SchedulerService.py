from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.scheduler import Scheduler
from src.usecase.submissions import SubmissionQueryModel


class SchedulerQueryModel(BaseModel):
    id: Optional[List[int]] = None
    submission_id: Optional[List[int]] = None
    reminded: Optional[bool] = None

    created_at: Optional[List[datetime]] = None
    created_be: Optional[datetime] = None
    created_af: Optional[datetime] = None

    updated_at: Optional[List[datetime]] = None
    updated_be: Optional[datetime] = None
    updated_af: Optional[datetime] = None

    remind_at: Optional[List[datetime]] = None
    remind_be: Optional[datetime] = None
    remind_af: Optional[datetime] = None

    submission: Optional[SubmissionQueryModel] = None


class SchedulerService(ABC):
    @abstractmethod
    async def fetch_all(self, query: SchedulerQueryModel) -> List[Scheduler]:
        raise NotImplementedError
