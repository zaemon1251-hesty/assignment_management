from pydantic.dataclasses import dataclass
from typing import Optional

from src.domain.assignments.AssignmentState import ASSIGNMENT_STATE, assignment_state
from src.domain.courses.CourseModel import Course


@dataclass(init=False, eq=True, frozen=True)
class Assignment:
    """assignment represents your collection of assignment as an entity."""

    def __init__(
        self,
        id: int,
        title: str,
        url: str,
        state: Optional[assignment_state] = ASSIGNMENT_STATE.ALIVE,
        course: Optional[Course] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: int = id
        self.title: str = title
        self.url: int = url
        self.state: assignment_state = state
        self.course: Optional[Course] = course
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
