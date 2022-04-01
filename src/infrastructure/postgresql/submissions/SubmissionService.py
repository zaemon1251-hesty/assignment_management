from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy import or_, and_
from src.domain.submission import Submission
from src.usecase.submissions import SubmissionService, SubmissionQueryModel
from src.infrastructure.postgresql.submissions import SubmissionOrm
from src.infrastructure.postgresql.assignments import AssignmentOrm
from src.infrastructure.postgresql.courses import CourseOrm
from src.usecase.assignments.AssignmentService import AssignmentQueryModel
from src.infrastructure.postgresql.BaseService import make_conditions
from usecase.courses.CourseService import CourseQueryModel


class SubmissionServiceImpl(SubmissionService):
    """Submission Service with postgreSQL

    Args:
        session (sqlalchemy.orm.Session): セッション
    """

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch_all(self, query: SubmissionQueryModel) -> List[Submission]:
        targets = dict(query) if query is not None else {}
        assignment_targets = dict(query.assignment) \
            if query is not None and query.assignment is not None else {}
        course_targets = dict(query.assignment.course) \
            if query.assignment is not None and query.assignment.course is not None else {}
        try:
            and_filters = []
            q = self.session.query(SubmissionOrm)

            for attr, value in targets.items():
                if isinstance(value, AssignmentQueryModel):
                    continue
                and_filters.append(make_conditions(SubmissionOrm, attr, value))

            for attr, value in assignment_targets.items():
                if isinstance(value, CourseQueryModel):
                    continue
                and_filters.append(make_conditions(AssignmentOrm, attr, value))

            for attr, value in course_targets.items():
                and_filters.append(make_conditions(CourseOrm, attr, value))

            q = q.filter(and_(*and_filters))
            q = q.order_by(SubmissionOrm.updated_at)
            submission_orms = q.all()

            return list(
                map(
                    lambda submission_orm: submission_orm.to_domain(),
                    submission_orms
                )
            ) if len(submission_orms) > 0 else []
        except Exception:
            raise
