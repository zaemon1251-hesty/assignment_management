from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional

from src.domain.submissions.SubmissionModel import Submission


class Scheduler(BaseModel):
    """Scheduler represents what assignment should be reminded to whom at a certain time """

    id: int
    submission: Submission
    remind_at: int
    reminded: Optional[bool] = False
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    class Config:
        orm_mode = True
        validate_assignment = True
