from datetime import datetime
from enum import Enum
from typing import Optional
from src.domain import OrmBase
from src.domain.course import Course


class ASSIGNMENT_STATE(Enum):
    ALIVE = 1
    DEAD = 2

    def __str__(self):
        return self.name


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
