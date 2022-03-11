from typing import Union
from domain import User
from domain import Course
from domain import Assignment
from domain import Submission
from domain import Scheduler

DOMAINS = Union[
    User,
    Course,
    Assignment,
    Submission,
    Scheduler
]
