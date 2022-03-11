from abc import ABC, abstractmethod
from typing import List, Optional

from domain.assignment import Assignment
from domain.submission import Submission
from domain.user import User


class SubmissionRepository(ABC):
    """submission"""
    @abstractmethod
    async def fetch(self, id: int) -> Optional[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, domain: Optional[Submission], user: Optional[User], assignment: Optional[Assignment]) -> List[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError
