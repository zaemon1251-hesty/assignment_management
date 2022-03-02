from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.assignments.AssignmentModel import Assignment
from src.domain.submissions.SubmissionModel import Submission
from src.domain.submissions.SubmissionState import submission_state
from src.domain.users.UserModel import User


class SubmissionUseCase(ABC):
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
    async def change_status(id: int, state: submission_state) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def scraping_add(user: User) -> bool:
        raise NotImplementedError
