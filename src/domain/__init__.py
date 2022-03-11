from enum import Enum
from typing import Optional, Union

from .user import User, AuthedUser
from .course import Course
from .assignment import Assignment, ASSIGNMENT_STATE
from .submission import Submission, SUBMISSION_STATE, StateContradictedException
from .scheduler import Scheduler
from .UserRepository import UserRepository
from .CourseRepository import CourseRepository
from .AssignmentRepository import AssignmentRepository
from .SubmissionRepository import SubmissionRepository
from .SchedulerRepository import SchedulerRepository
from .exception import (
    TargetAlreadyExsitException,
    TargetNotFoundException,
    CredentialsException,
    UnauthorizedException,
)
