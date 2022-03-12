from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from src.domain import (
    Assignment,
    Course,
    Scheduler,
    SUBMISSION_STATE,
    User,
)


class NotifyDriver(ABC):
    """ driver (notify user a deadline of assignment) """

    @abstractmethod
    async def notify(self, user: User, assignemt: Assignment, state: SUBMISSION_STATE) -> None:
        raise NotImplementedError
