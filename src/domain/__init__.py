from enum import Enum
from typing import Union

from src.domain.users.UserModel import User
from src.domain.courses.CourseModel import Course
from src.domain.assignments.AssignmentModel import Assignment
from src.domain.submissions.SubmissionModel import Submission

from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


class OrmBase(BaseModel):
    # Common properties across orm models
    id: int

    # Pre-processing validator that evaluates lazy relationships before any other validation
    # NOTE: If high throughput/performance is a concern, you can/should probably apply
    #       this validator in a more targeted fashion instead of a wildcard in a base class.
    # This approach is by no means slow, but adds a minor amount of overhead
    # for every field
    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True
        validate_assignment = True


DOMAINS = Union[
    User,
    Course,
    Assignment,
    Submission,
]
