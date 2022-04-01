from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.assignment import Assignment
from src.usecase.courses.CourseService import CourseQueryModel


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


class AssignmentService(ABC):
    @abstractmethod
    async def fetch_all(self, query: AssignmentQueryModel) -> List[Assignment]:
        raise NotImplementedError
