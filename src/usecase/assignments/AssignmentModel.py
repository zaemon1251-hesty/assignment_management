from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.usecase.courses import CourseQueryModel


class AssignmentQueryModel(BaseModel):
    id: Optional[List[int]] = None
    course_id: Optional[List[int]] = None
    title: Optional[str] = None
    url: Optional[str] = None
    info: Optional[str] = None
    state: Optional[List[int]] = None
    end_at: Optional[List[datetime]] = None
    end_be: Optional[datetime] = None
    end_af: Optional[datetime] = None
    created_at: Optional[List[datetime]] = None
    created_be: Optional[datetime] = None
    created_af: Optional[datetime] = None
    updated_at: Optional[List[datetime]] = None
    updated_be: Optional[datetime] = None
    updated_af: Optional[datetime] = None
    course: Optional[CourseQueryModel] = None


class AssignmentCommandModel(BaseModel):
    """assignment represents your collection of assignment as an entity."""
    title: str = None
    url: str = None
    info: str = None
    state: int = None
    course_id: int = None
    end_at: datetime = None
