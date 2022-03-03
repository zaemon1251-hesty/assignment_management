from datetime import datetime
from typing import Optional
from src.domain import OrmBase

from src.domain.assignments.AssignmentState import ASSIGNMENT_STATE
from src.domain.courses.CourseModel import Course


class Assignment(OrmBase):
    """assignment represents your collection of assignment as an entity."""

    id: int
    title: str
    url: Optional[str]
    info: Optional[str]
    state: Optional[ASSIGNMENT_STATE] = ASSIGNMENT_STATE.ALIVE
    course: Optional[Course] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
