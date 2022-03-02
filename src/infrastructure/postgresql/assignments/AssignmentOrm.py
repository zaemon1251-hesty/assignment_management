from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional

from src.domain.assignments.AssignmentState import ASSIGNMENT_STATE, assignment_state
from src.domain.courses.CourseModel import Course


class Assignment(BaseModel):
    """assignment represents your collection of assignment as an entity."""

    id: int
    title: str
    url: str
    state: Optional[assignment_state] = ASSIGNMENT_STATE.ALIVE
    course: Optional[Course] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    class Config:
        orm_mode = True
