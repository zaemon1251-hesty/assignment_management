from pydantic.dataclasses import dataclass
from typing import Optional

from src.domain.assignments.AssignmentModel import Assignment
from src.domain.assignments.AssignmentState import ASSIGNMENT_STATE
from src.domain.submissions.SubmissionState import SUBMISSION_STATE, submission_state
from src.domain.users.UserModel import User


@dataclass(init=False, eq=True, frozen=True)
class Submission:
    """submission represents your registerd assignment as an entity."""

    def __init__(
        self,
        id: int,
        user: User,
        assignment: Assignment,
        state: Optional[submission_state] = SUBMISSION_STATE.NORMAL,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: int = id
        self.user: User = user,
        self.assignment: Assignment = assignment,
        self.state: submission_state = state
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

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
