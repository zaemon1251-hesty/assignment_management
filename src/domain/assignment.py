from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from domain.base import OrmBase
from domain import course
from domain.course import Course


class ASSIGNMENT_STATE(int, Enum):
    ALIVE = 1
    DEAD = 2

    def __str__(self):
        return self.name


class Assignment(OrmBase):
    """assignment represents your collection of assignment as an entity."""

    title: str
    url: Optional[str]
    info: Optional[str]
    state: Optional[ASSIGNMENT_STATE] = ASSIGNMENT_STATE.ALIVE
    course_id: int
    end_at: datetime = datetime.fromtimestamp(0) + timedelta(days=10**5)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    course: Optional[Course]
