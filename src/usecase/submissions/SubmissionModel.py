from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.submission import Submission
from src.usecase.assignments import AssignmentQueryModel


class SubmissionQueryModel(BaseModel):
    id: Optional[List[int]] = None
    user_id: Optional[List[int]] = None
    assignment_id: Optional[List[int]] = None
    state: Optional[List[int]] = None
    created_at: Optional[List[datetime]] = None
    updated_at: Optional[List[datetime]] = None
    created_be: Optional[datetime] = None
    created_af: Optional[datetime] = None
    updated_be: Optional[datetime] = None
    updated_af: Optional[datetime] = None
    assignment: Optional[AssignmentQueryModel] = None


class SubmissionCommandModel(BaseModel):
    """submission represents your registerd assignment as an entity."""

    user_id: int = None
    assignment_id: int = None
    state: int = None
