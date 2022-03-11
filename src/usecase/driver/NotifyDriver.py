from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from domain.assignment import Assignment
from domain.course import Course
from domain.scheduler import Scheduler
from domain.submission import SUBMISSION_STATE
from domain.user import User


class NotifyDriver(ABC):
    """ driver (notify user a deadline of assignment) """

    @abstractmethod
    async def notify(self, user: User, assignemt: Assignment, state: SUBMISSION_STATE) -> None:
        raise NotImplementedError
