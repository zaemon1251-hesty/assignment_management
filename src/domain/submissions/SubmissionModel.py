from dataclasses import dataclass
from typing import Optional

from src.domain.assignments.AssignmentModel import Assignment
from src.domain.submissions.SubmissionState import SUBMISSION_STATE, submission_state
from src.domain.users.UserModel import User


@dataclass(init=False, eq=True, frozen=True)
class Submission:
    """submission represents your registerd assignment as an entity."""

    def __init__(
        self,
        id: str,
        user: User,
        assignment: Assignment,
        state: Optional[submission_state] = SUBMISSION_STATE.NORMAL,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        user: User = user,
        assignment: Assignment = assignment,
        self.state: submission_state = state
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
