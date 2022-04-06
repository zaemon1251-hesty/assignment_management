from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy import or_, and_
from src.domain.scheduler import Scheduler
from src.usecase.schedulers import SchedulerService, SchedulerQueryModel
from src.infrastructure.postgresql.schedulers import SchedulerOrm
from src.infrastructure.postgresql.assignments import AssignmentOrm
from src.infrastructure.postgresql.submissions import SubmissionOrm
from src.infrastructure.postgresql.courses import CourseOrm
from src.usecase.assignments import AssignmentQueryModel
from src.infrastructure.postgresql.BaseService import make_conditions
from src.usecase.courses import CourseQueryModel
from src.usecase.submissions import SubmissionQueryModel


class SchedulerServiceImpl(SchedulerService):
    """Scheduler Service with postgreSQL

    Args:
        session (sqlalchemy.orm.Session): セッション
    """

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch_all(self, query: SchedulerQueryModel) -> List[Scheduler]:
        targets = {}
        submission_targets = {}
        assignment_targets = {}
        course_targets = {}

        if query is not None:
            targets = query.dict()
            if query.submission is not None:
                submission_targets = query.submission.dict()
                if query.submission.assignment is not None:
                    assignment_targets = query.submission.assignment.dict()
                    if query.submission.assignment.course is not None:
                        course_targets = query.submission.assignment.course.dict()

        try:
            and_filters = []
            q = self.session.query(SchedulerOrm)

            for attr, value in targets.items():
                if isinstance(value, SubmissionQueryModel) or value is None:
                    continue
                and_filters.append(make_conditions(SchedulerOrm, attr, value))

            for attr, value in submission_targets.items():
                if isinstance(value, AssignmentQueryModel) or value is None:
                    continue
                and_filters.append(make_conditions(SubmissionOrm, attr, value))

            for attr, value in assignment_targets.items():
                if isinstance(value, CourseQueryModel) or value is None:
                    continue
                and_filters.append(make_conditions(AssignmentOrm, attr, value))

            for attr, value in course_targets.items():
                if value is None:
                    continue
                and_filters.append(make_conditions(CourseOrm, attr, value))

            q = q.filter(and_(*and_filters))
            q = q.order_by(SchedulerOrm.updated_at)
            scheduler_orms = q.all()

            return list(
                map(
                    lambda scheduler_orm: scheduler_orm.to_domain(),
                    scheduler_orms
                )
            ) if len(scheduler_orms) > 0 else []
        except Exception:
            raise
