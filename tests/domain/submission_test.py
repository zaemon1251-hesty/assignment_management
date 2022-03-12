import tests
from datetime import datetime
from src.domain.assignment import ASSIGNMENT_STATE
from src.domain.submission import SUBMISSION_STATE
from src.domain import Submission, Assignment, Course, StateContradictedException, User
import pytest


class SubmissionTest:

    def __init__(self):
        self.user = User(
            id=1,
            name="test",
            email="test@example.com",
            disabled=False)
        self.course = Course(id=1, url="http://example.com", title="テストのコースです")
        self.assignment = Assignment(
            id=1,
            course_id=1,
            state=ASSIGNMENT_STATE.ALIVE,
            end_at=datetime.fromisoformat("2022/03/12"))
        self.submission = Submission(
            id=1,
            user_id=1,
            assignment_id=1,
            state=SUBMISSION_STATE.NORMAL,
            assignment=self.assignment)

    def test_validate_submission(self):
        assert self.submission.id == 1
        assert self.submission.state.value == 1

    def test_change_submission_state_nocontradict(self):
        self.submission.state = SUBMISSION_STATE.DANGER

    def test_change_submission_state_contradict(self):
        with pytest.raises(StateContradictedException):
            self.submission.state = SUBMISSION_STATE.EXPIRED
