from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignment import Assignment
from src.domain.submission import Submission
from src.domain.user import User


class SubmissionRepository(ABC):
    """submission"""
    @abstractmethod
    async def fetch(id: int) -> Optional[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(domain: Optional[Submission], user: Optional[User], assignment: Optional[Assignment]) -> List[Submission]:
        raise NotImplementedError

    @abstractmethod
    async def add(domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def update(domain: Submission) -> Submission:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> Submission:
        raise NotImplementedError