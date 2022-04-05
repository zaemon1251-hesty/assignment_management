from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.course import Course
from .CourseModel import CourseQueryModel


class CourseService(ABC):
    @abstractmethod
    async def fetch_all(self, query: CourseQueryModel) -> List[Course]:
        raise NotImplementedError
