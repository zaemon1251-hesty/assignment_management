from enum import Enum
from typing import Union

from src.domain.users.UserModel import User
from src.domain.courses.CourseModel import Course
from src.domain.assignments.AssignmentModel import Assignment
from src.domain.submissions.SubmissionModel import Submission


DOMAINS = Union[
    User,
    Course,
    Assignment,
    Submission,
]