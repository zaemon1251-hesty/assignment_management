from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from .AssignmentModel import AssignmentQueryModel
from src.domain import Assignment


class AssignmentService(ABC):
    @abstractmethod
    async def fetch_all(self, query: AssignmentQueryModel) -> List[Assignment]:
        raise NotImplementedError
