from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from src.domain.assignment import Assignment
from src.domain.course import Course
from src.domain.scheduler import Scheduler
from src.domain.submission import SUBMISSION_STATE
from src.domain.user import User


class NotifyDriver(ABC):
    """ driver (notify user a deadline of assignment) """

    @abstractmethod
    async def notify(self, user: User, assignemt: Assignment, state: SUBMISSION_STATE) -> None:
        raise NotImplementedError
