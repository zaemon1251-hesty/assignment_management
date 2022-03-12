from typing import Union
from src.domain import User
from src.domain import Course
from src.domain import Assignment
from src.domain import Submission
from src.domain import Scheduler

DOMAINS = Union[
    User,
    Course,
    Assignment,
    Submission,
    Scheduler
]
