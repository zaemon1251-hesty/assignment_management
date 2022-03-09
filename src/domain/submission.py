from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import validator

from src.domain import OrmBase
from src.domain.assignment import Assignment, ASSIGNMENT_STATE
from src.domain.exception import StateContradictedException
from src.domain.user import User


class SUBMISSION_STATE(Enum):
    NORMAL = 1
    DANGER = 2
    SUBMITTED = 3
    EXPIRED = 4

    def __str__(self):
        return self.name


class Submission(OrmBase):
    """submission represents your registerd assignment as an entity."""

    user_id: int
    assignment_id: int
    state: Optional[SUBMISSION_STATE] = SUBMISSION_STATE.NORMAL
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def is_already_expired(state: SUBMISSION_STATE,
                           assignment_state: ASSIGNMENT_STATE) -> bool:
        """ this condition is not xpected
            system should prevent this in usecase layer
        """
        return (
            state == SUBMISSION_STATE.NORMAL or
            state == SUBMISSION_STATE.DANGER
        ) and assignment_state == ASSIGNMENT_STATE.DEAD

    @staticmethod
    def is_still_alive(state: SUBMISSION_STATE,
                       assignment_state: ASSIGNMENT_STATE) -> bool:
        """ this condition is not expected
            system should prevent this in usecase layer
        """
        return state == SUBMISSION_STATE.EXPIRED and \
            assignment_state == ASSIGNMENT_STATE.ALIVE

    @validator("state")
    async def _validate_state(cls, v, values, **kwargs):
        if "assignment" in values and "state" in dict(values["assignment"]):
            if cls.is_already_expired(v, values["assignment"].state) or \
                    cls.is_still_alive(v, values["assignment"].state):
                raise StateContradictedException(
                    "submission_state:%s isn't acceptable because og the related assignment state: %s" % (v, values[
                        "assignment"].state))
        return v
