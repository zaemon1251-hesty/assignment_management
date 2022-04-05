from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.submission import Submission
from .SubmissionModel import SubmissionQueryModel


class SubmissionService(ABC):
    @abstractmethod
    async def fetch_all(self, query: SubmissionQueryModel) -> List[Submission]:
        raise NotImplementedError
