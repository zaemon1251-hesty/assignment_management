from datetime import datetime
from typing import Optional
from src.domain import OrmBase

from src.domain.submission import Submission


class Scheduler(OrmBase):
    """Scheduler represents what assignment should be reminded to whom at a certain time """

    submission_id: int
    remind_at: int
    reminded: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
