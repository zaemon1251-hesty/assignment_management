from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CourseQueryModel(BaseModel):
    id: Optional[List[int]] = None
    title: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[List[datetime]] = None
    updated_at: Optional[List[datetime]] = None
    created_be: Optional[datetime] = None
    created_af: Optional[datetime] = None
    updated_be: Optional[datetime] = None
    updated_af: Optional[datetime] = None


class CourseCommandModel(BaseModel):
    title: str = None
    url: str = None
