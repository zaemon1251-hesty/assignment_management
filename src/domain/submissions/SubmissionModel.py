from datetime import datetime
from typing import Optional

from src.domain import OrmBase
from src.domain.assignments.AssignmentModel import Assignment
from src.domain.assignments.AssignmentState import ASSIGNMENT_STATE
from src.domain.submissions.SubmissionState import SUBMISSION_STATE
from src.domain.users.UserModel import User


class Submission(OrmBase):
    """submission represents your registerd assignment as an entity."""

    id: int
    user: User
    assignment: Assignment
    state: Optional[SUBMISSION_STATE] = SUBMISSION_STATE.NORMAL
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_already_expired(self) -> bool:
        """ this condition is not expected
            system should prevent this in usecase layer
        """
        return (
            self.state == SUBMISSION_STATE.NORMAL or
            self.state == SUBMISSION_STATE.DANGER
        ) and self.assignment.state == ASSIGNMENT_STATE.DEAD

    def is_still_alive(self) -> bool:
        """ this condition is not expected
            system should prevent this in usecase layer
        """
        return self.state == SUBMISSION_STATE.EXPIRED and \
            self.assignment.state == ASSIGNMENT_STATE.ALIVE
